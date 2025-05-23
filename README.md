# tmm-webinfo

Webinfo for puzzle hunts stolen (borrowed) from [TMM](https://github.com/Tabor-Mladych-Matematiku/tmm-webinfo) and translated to English.

## How to run

### Before first run

1. Install the requirements:
   ```shell
   py -m pip install -r requirements.txt
   ```
2. Rename `tmm_webinfo.example.yaml` to `tmm_webinfo.yaml` and fill in the details (for debugging using a local SQLite database, remove
   the `db` section).

3. Prepare the database:
    ```shell
    py create_db.py
    ```

### Run (for development)

```shell
py -m flask --app tmm_webinfo run 
```
or
```shell
flask --app tmm_webinfo run
```

For production:
```shell
gunicorn -w 4 -b 0.0.0.0:8080 tmm_webinfo:app
sudo -E /home/tumi/anaconda3/envs/puzzle/bin/gunicorn -w 4 -b 0.0.0.0:443 --certfile=/etc/letsencrypt/live/puzzle.esn-tumi.de/fullchain.pem --keyfile=/etc/letsencrypt/live/puzzle.esn-tumi.de/privkey.pem tmm_webinfo:app
```

## Database
https://phoenixnap.com/kb/mysql-docker-container
You can set up mysql database in docker by using the following commands:
```shell
docker pull mysql/mysql-server:latest
docker run --name=mysql-tmm -p 3307:3306 -e MYSQL_ROOT_PASSWORD=MyNewPass -d mysql/mysql-server:latest
docker exec -it mysql-tmm bash
mysql -u root -p
CREATE USER 'webinfo'@'%' IDENTIFIED BY 'my_password';
GRANT ALL PRIVILEGES ON *.* TO 'webinfo'@'%';
CREATE DATABASE testDB;
```

## Deployment

The [PythonAnywhere](https://eu.pythonanywhere.com/) free hosting can be used to deploy the app. They have a [A beginner's guide to building a simple database-backed Flask website on PythonAnywhere](https://blog.pythonanywhere.com/121/) which can serve as a reference for creating an account there and setting up the database. However, it is not a tutorial for deploying an existing project so instead of writing the code of the app according to the tutorial, this repository can be cloned (using a console) and the *WSGI configuration file* updated accordingly to set `project_home` and import `from tmm_webinfo import app as application`.

## Notes
What is needed to do in order to run again a TUMi puzzle hunt from the last semester:
1. Update the puzzles on [TUMi Github](https://github.com/esn-tumi/puzzle-hunt)
2. Create a form for the team registration and a QR code with [some static QR code generator](https://www.qrcode-monkey.com)
3. Update the `puzzle_hunt.csv` in the puzzle repo with solutions, hints and locations
4. Log in to the puzzle machine on Azure (should be already connected to the domain puzzle.esn-tumi.de and have allowed https traffic)
5. Update certificates if necessary: `sudo certbot renew`
6. Update `tmm-webinfo/tmm_webinfo.yaml` with an admin password and database data
7. Set up the database (an old docker container might still be active)
8. Start the app encrypted with certificates, ideally in tmux
9. Create the puzzle hunt in the app from `puzzle_hunt.csv`
10. Create the teams from the participants entries in the forms
When participants first get the link, the app might crash if it doesn't have enough resources, but will recover again (or just start it again, the data stay in the db).
