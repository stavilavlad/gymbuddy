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


@app.route("/")
def index():
    return render_template("index.html", active_status_home="active")


@app.route("/exercises/<muscle_group>")
def exercises(muscle_group):
    mgroup = muscle_group
    if muscle_group == "back":
        rows = db.execute("SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part IN ('Lats', 'Traps', 'Middle Back', 'Lower Back') AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' ORDER BY body_part, CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;")
    elif muscle_group == "legs":
        rows = db.execute("SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part IN ('Adductors', 'Abductors', 'Hamstrings', 'Quadriceps') AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' ORDER BY body_part, CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;")
    else:
        rows = db.execute(
            "SELECT exercises.id, exercises.exercise_name, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.description_url, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE body_part = ? AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '' AND exercises.description <> '' ORDER BY CASE WHEN exercises.level = 'Beginner' THEN 1 WHEN exercises.level = 'Intermediate' THEN 2 WHEN exercises.level = 'Expert' THEN 3 ELSE 4 END, exercises.exercise_name;", muscle_group.capitalize())

    return render_template("exercises.html", active_status_exercises="active", rows=rows, mgroup=mgroup)


@app.route("/exercises_individual/<id>")
def individual_exercise(id):
    ex_id = id
    rows = db.execute(
        "SELECT exercises.id, exercises.exercise_name, exercises.description, exercises.type, exercises.body_part, exercises.equipment, exercises.level, images_dataset.description_url, images_dataset.exercise_image1, images_dataset.exercise_image2 FROM exercises JOIN images_dataset ON exercises.exercise_name = images_dataset.exercise_name WHERE exercises.id = ? AND images_dataset.exercise_image1 IS NOT NULL AND images_dataset.exercise_image1 <> '' AND images_dataset.exercise_image2 <> '';", id)
    return render_template("individual_exercise.html", rows=rows, active_status_exercises="active")
