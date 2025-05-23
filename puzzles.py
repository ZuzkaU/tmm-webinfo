from flask import request, redirect, flash, Blueprint

from codes import get_arrival_codes, get_solution_codes
from db_model import Puzzle, db, PuzzlePrerequisite, Puzzlehunt
from helpers import render, admin_required
from hints import get_hints

puzzles = Blueprint('puzzles', __name__, template_folder='templates', static_folder='static')


@puzzles.route('/puzzles')
@admin_required
def puzzles_list():
    puzzles = Puzzle.query.filter_by(id_puzzlehunt=Puzzlehunt.get_current_id()).order_by(Puzzle.order).all()
    return render("puzzles.html", puzzles=puzzles)


@puzzles.route('/puzzles/new', methods=("GET", "POST"))
@admin_required
def puzzles_new():
    if request.method == "POST":
        puzzle = Puzzle(Puzzlehunt.get_current_id(), request.form["puzzle"], request.form["assignment"], request.form["order"])
        db.session.add(puzzle)
        db.session.commit()
        return redirect(f"/puzzles/{puzzle.id_puzzle}")
    order = Puzzle.query.filter_by(id_puzzlehunt=Puzzlehunt.get_current_id()).count() + 1
    return render("puzzle_edit.html", order=order)


@puzzles.route('/puzzles/<id_puzzle>', methods=("GET", "POST"))
@admin_required
def puzzles_edit(id_puzzle):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")

    if request.method == "POST":
        puzzle.puzzle = request.form["puzzle"]
        puzzle.assignment = request.form["assignment"]
        puzzle.order = request.form["order"]
        db.session.add(puzzle)
        db.session.commit()
        return redirect("/puzzles")
    else:
        arrival_codes = get_arrival_codes(id_puzzle)
        solution_codes = get_solution_codes(id_puzzle)
        hints = get_hints(id_puzzle)
        return render("puzzle_edit.html", puzzle=puzzle, arrival_codes=arrival_codes, solution_codes=solution_codes, hints=hints)


@puzzles.route('/puzzles/<id_puzzle>/delete', methods=("POST",))
@admin_required
def puzzles_delete(id_puzzle):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")

    db.session.delete(puzzle)
    db.session.commit()
    flash(f'Puzzle "{puzzle.puzzle}" deleted.', "success")
    return redirect("/puzzles")


@puzzles.route('/puzzles/<id_new_puzzle>/prerequisites/new', methods=("GET", "POST"))
@admin_required
def prerequisites_new(id_new_puzzle):
    puzzle = Puzzle.query.get(id_new_puzzle)
    if request.method == "POST":
        prerequisite = PuzzlePrerequisite(request.form["prerequisite"], id_new_puzzle)
        db.session.add(prerequisite)
        db.session.commit()
        return redirect(f"/puzzles/{id_new_puzzle}")
    else:
        prerequisites_ids = [p.id_puzzle for p in puzzle.get_prerequisites()]
        other_puzzles = Puzzle.query.filter_by(id_puzzlehunt=Puzzlehunt.get_current_id())\
            .filter(Puzzle.id_puzzle.not_in(prerequisites_ids + [puzzle.id_puzzle])).all()
        return render("prerequisite_edit.html", puzzle=puzzle, other_puzzles=other_puzzles)


@puzzles.route('/puzzles/<id_new_puzzle>/prerequisites/<id_previous_puzzle>/delete', methods=("POST",))
@admin_required
def prerequisites_delete(id_new_puzzle, id_previous_puzzle):
    prerequisite = PuzzlePrerequisite.query.get((id_previous_puzzle, id_new_puzzle))
    if prerequisite is not None:
        db.session.delete(prerequisite)
        db.session.commit()
        flash(f'Prerequisite deleted.', "success")
    else:
        flash(f'Prerequisite not found.', "warning")
    return redirect(f"/puzzles/{id_new_puzzle}")
