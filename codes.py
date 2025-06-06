from flask import request, redirect, flash, Blueprint

from db_model import Puzzle, db, Code, ArrivalCode, SolutionCode
from helpers import render, admin_required

codes = Blueprint('codes', __name__, template_folder='templates', static_folder='static')


# Code normalization


LETTERS_NODIA = "acdeeinorstuuyz"
LETTERS_DIA = "áčďéěíňóřšťúůýž"

# A translation table usable with `str.translate` to rewrite characters with dia to the ones without them.
REMOVE_DIA = str.maketrans(LETTERS_DIA + LETTERS_DIA.upper(), LETTERS_NODIA + LETTERS_NODIA.upper())


def remove_diacritics(text: str):
    return text.translate(REMOVE_DIA)


def compare_codes(user_code: str, correct_code: str):
    user_code = remove_diacritics(user_code).lower().strip()
    correct_code = remove_diacritics(correct_code).lower().strip()
    return user_code == correct_code


# Puzzlehunt codes


def get_codes(id_puzzlehunt):
    return Code.query.filter_by(id_puzzlehunt=id_puzzlehunt).all()


@codes.route('/puzzlehunts/<id_puzzlehunt>/codes/new', methods=("GET", "POST"))
@admin_required
def codes_new(id_puzzlehunt):
    if request.method == "POST":
        code = Code(id_puzzlehunt, request.form["code"], request.form["message"])
        db.session.add(code)
        db.session.commit()
        return redirect(f"/puzzlehunts/{id_puzzlehunt}")
    return render("code_edit.html", heading="Add code to puzzle hunt", back_url=f"/puzzlehunts/{id_puzzlehunt}")


@codes.route('/puzzlehunts/<id_puzzlehunt>/codes/<id_code>', methods=("GET", "POST"))
@admin_required
def codes_edit(id_puzzlehunt, id_code):
    code = Code.query.get(id_code)
    if code is None:
        flash(f"The code with id_code={id_code} doesn't exist.", "warning")
        return redirect(f"/puzzlehunts/{id_puzzlehunt}")

    if request.method == "POST":
        code.code = request.form["code"]
        code.message = request.form["message"]
        db.session.add(code)
        db.session.commit()
        return redirect(f"/puzzlehunts/{id_puzzlehunt}")
    else:
        return render("code_edit.html", heading="Edit code", back_url=f"/puzzlehunts/{id_puzzlehunt}", code=code)


@codes.route('/puzzlehunts/<id_puzzlehunt>/codes/<id_code>/delete', methods=("POST",))
@admin_required
def codes_delete(id_puzzlehunt, id_code):
    code = Code.query.get(id_code)
    if code is None:
        flash(f"The code with id_code={id_code} doesn't exist.", "warning")
        return redirect(f"/puzzlehunts/{id_puzzlehunt}")

    db.session.delete(code)
    db.session.commit()
    flash(f'Code "{code.code}" deleted.', "success")
    return redirect(f"/puzzlehunts/{id_puzzlehunt}")


# Arrival codes


def get_arrival_codes(id_puzzle):
    return ArrivalCode.query.filter_by(id_puzzle=id_puzzle).all()


@codes.route('/puzzles/<id_puzzle>/arrival_codes/new', methods=("GET", "POST"))
@admin_required
def arrival_codes_new(id_puzzle):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")

    if request.method == "POST":
        code = ArrivalCode(id_puzzle, request.form["code"], request.form["message"])
        db.session.add(code)
        db.session.commit()
        return redirect(f"/puzzles/{id_puzzle}")
    return render("code_edit.html", heading="Add code to open a puzzle", back_url=f"/puzzles/{id_puzzle}", puzzle=puzzle)


@codes.route('/puzzles/<id_puzzle>/arrival_codes/<id_arrival_code>', methods=("GET", "POST"))
@admin_required
def arrival_codes_edit(id_puzzle, id_arrival_code):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")
    arrival_code = ArrivalCode.query.get(id_arrival_code)
    if arrival_code is None:
        flash(f"Code with id_arrival_code={id_arrival_code} doesn't exist.", "warning")
        return redirect(f"/puzzles/{id_puzzle}")

    if request.method == "POST":
        arrival_code.code = request.form["code"]
        arrival_code.message = request.form["message"]
        db.session.add(arrival_code)
        db.session.commit()
        return redirect(f"/puzzles/{id_puzzle}")
    else:
        return render("code_edit.html", heading="Edit code", back_url=f"/puzzles/{id_puzzle}", code=arrival_code, puzzle=puzzle)


@codes.route('/puzzles/<id_puzzle>/arrival_codes/<id_arrival_code>/delete', methods=("POST",))
@admin_required
def arrival_codes_delete(id_puzzle, id_arrival_code):
    arrival_code = ArrivalCode.query.get(id_arrival_code)
    if arrival_code is None:
        flash(f"Code with id_arrival_code={id_arrival_code} doesn't exist.", "warning")
        return redirect(f"/puzzles/{id_puzzle}")

    db.session.delete(arrival_code)
    db.session.commit()
    flash(f'Code "{arrival_code.code}" deleted.', "success")
    return redirect(f"/puzzles/{id_puzzle}")


# Solution codes


def get_solution_codes(id_puzzle):
    return SolutionCode.query.filter_by(id_puzzle=id_puzzle).all()


@codes.route('/puzzles/<id_puzzle>/solution_codes/new', methods=("GET", "POST"))
@admin_required
def solution_codes_new(id_puzzle):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")

    if request.method == "POST":
        code = SolutionCode(id_puzzle, request.form["code"], request.form["message"])
        db.session.add(code)
        db.session.commit()
        return redirect(f"/puzzles/{id_puzzle}")
    return render("code_edit.html", heading="Add puzzle solution", back_url=f"/puzzles/{id_puzzle}", puzzle=puzzle)


@codes.route('/puzzles/<id_puzzle>/solution_codes/<id_solution_code>', methods=("GET", "POST"))
@admin_required
def solution_codes_edit(id_puzzle, id_solution_code):
    puzzle = Puzzle.query.get(id_puzzle)
    if puzzle is None:
        flash(f"Puzzle with id_puzzle={id_puzzle} doesn't exist.", "warning")
        return redirect("/puzzles")
    solution_code = SolutionCode.query.get(id_solution_code)
    if solution_code is None:
        flash(f"Solution with id_solution_code={id_solution_code} doesn't exist.", "warning")
        return redirect(f"/puzzles/{id_puzzle}")

    if request.method == "POST":
        solution_code.code = request.form["code"]
        solution_code.message = request.form["message"]
        db.session.add(solution_code)
        db.session.commit()
        return redirect(f"/puzzles/{id_puzzle}")
    else:
        return render("code_edit.html", heading="Edit solution", back_url=f"/puzzles/{id_puzzle}", code=solution_code, puzzle=puzzle)


@codes.route('/puzzles/<id_puzzle>/solution_codes/<id_solution_code>/delete', methods=("POST",))
@admin_required
def solution_codes_delete(id_puzzle, id_solution_code):
    solution_code = SolutionCode.query.get(id_solution_code)
    if solution_code is None:
        flash(f"Solution with id_solution_code={id_solution_code} doesn't exist.", "warning")
        return redirect(f"/puzzles/{id_puzzle}")

    db.session.delete(solution_code)
    db.session.commit()
    flash(f'Solution "{solution_code.code}" deleted.', "success")
    return redirect(f"/puzzles/{id_puzzle}")

