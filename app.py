import os
import csv
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///exercises.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    success = False
    error = False
    succ_message = ""

    # Sign up
    if request.method == "POST" and request.form.get("signup_username"):
        username = request.form.get("signup_username")
        password = request.form.get("signup_password")
        db_usernames = db.execute("SELECT username FROM users;")
        list_usernames = []
        for i in range(len(db_usernames)):
            list_usernames.append(db_usernames[i]["username"])

        if username in list_usernames:
            err_message = "Username already exists!"
            error = True
            return render_template("index.html", active_status_home="active", error=error, err_message=err_message)

        succ_message = "Signed Up Succesfully!"
        success = True
        db.execute("INSERT INTO users(username, hash) VALUES (?,?)",
                   username, generate_password_hash(password))

    # Log in
    elif request.method == "POST" and request.form.get("username"):

        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            err_message = "Incorrect username or password!"
            error = True
            return render_template("index.html", active_status_home="active", error=error, err_message=err_message)

        succ_message = "Logged In!"
        success = True

        session["user_id"] = rows[0]["id"]

    return render_template("index.html", active_status_home="active", success=success, succ_message=succ_message)


@app.route("/exercises/<muscle_group>")
def exercises(muscle_group):
    mgroup = muscle_group
    if muscle_group == "back":
        rows = db.execute("SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part IN ('Lats', 'Traps', 'Middle Back', 'Lower Back') AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' AND exercises.description <> '' ORDER BY body_part, CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;")
    elif muscle_group == "legs":
        rows = db.execute("SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part IN ('Adductors', 'Abductors', 'Hamstrings', 'Quadriceps') AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' AND exercises.description <> '' ORDER BY body_part, CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;")
    else:
        rows = db.execute(
            "SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.description_url, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part = ? AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' AND exercises.description <> '' ORDER BY CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;", muscle_group.capitalize())

    return render_template("exercises.html", active_status_exercises="active", rows=rows, mgroup=mgroup)


@app.route("/exercises_individual/<id>")
def individual_exercise(id):
    rows = db.execute(
        "SELECT exercises.id, exercises.exercise_name, exercises.description, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.description_url, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE exercises.id = ? AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '';", id)
    return render_template("individual_exercise.html", rows=rows, active_status_exercises="active")


@app.route("/profile/<e_id>", methods=["GET", "POST"])
def profile(e_id):

    if e_id == "favourites":
        rows = db.execute(
            "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])
        return render_template("favourites.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")

    elif request.method == "POST" and request.form.get("fav") == "fav":
        print("adauga")
        print(request.form.get("fav"))
        print(e_id)
        db.execute("INSERT INTO user_exercise(user_id, exercise_id) VALUES (?,?)",
                   session["user_id"], e_id)
        rows = db.execute(
            "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])
        return render_template("favourites.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")

    elif request.method == "POST" and request.form.get("remove") == "remove":
        print("sterge")
        db.execute("DELETE FROM user_exercise WHERE user_id = ? AND exercise_id = ?",
                   session["user_id"], e_id)
    print("e doar get")
    rows = db.execute(
        "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])

    return render_template("favourites.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
