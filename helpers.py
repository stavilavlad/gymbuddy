import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={
                                "User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(
            response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

    # if e_id == "favourites":
    #     rows = db.execute(
    #         "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])
    #     return render_template("exercises.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")

    # if request.method == "POST":
    #     exercises_list = []
    #     rows = db.execute(
    #         "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])
    #     for row in rows:
    #         exercises_list.append(row["exercise_id"])
    #     print(exercises_list)

    #     if e_id in exercises_list:
    #         print(exercises_list)
    #         return render_template("exercises.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")

    #     db.execute("INSERT INTO user_exercise(user_id, exercise_id) VALUES (?,?)",
    #                session["user_id"], e_id)

    #     if e_id == "favourites":
    #     rows = db.execute(
    #         "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])
    #     return render_template("exercises.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")

    # db.execute("INSERT INTO user_exercise(user_id, exercise_id) VALUES (?,?)",
    #            session["user_id"], e_id)

    # rows = db.execute(
    #     "SELECT * FROM user_exercise JOIN exercises ON user_exercise.exercise_id = exercises.id JOIN images_dataset ON images_dataset.exercise_name = exercises.exercise_name WHERE user_exercise.user_id = ?", session["user_id"])

    # return render_template("exercises.html",  mgroup="FAVOURITE", rows=rows, active_status_favourites="active")
