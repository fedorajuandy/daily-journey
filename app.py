# Staff's Solution as reference

import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

import re
from datetime import datetime

from helpers import apology, login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show locked page"""
    # Gets data from database
    j = db.execute("SELECT * FROM journeys WHERE date = (SELECT CONVERT(VARCHAR(10), GETDATE(), 105)) AND user_id = ?", session["user_id"])
    journey = j[0]["journey"]
    m = db.execute("SELECT AVERAGE(mood) AS mood FROM general WHERE user_id = ? GROUP BY user_id", session["user_id"])
    w = db.execute("SELECT COUNTA(weather) AS weather FROM general WHERE user_id = ? GROUP BY user_id", session["user_id"])
    p = db.execute("SELECT COUNTA(mentioned) AS person FROM general WHERE user_id = ? GROUP BY user_id", session["user_id"])

    # If there is no data yet
    if len(m) >= 1:
        mood = m[0]["mood"]
        weather = w[0]["weather"]
        mentioned = p[0]["mentioned"]
    else:
        mood = 0
        weather = "None"
        mentioned = "Nobody :( are you lonely?"

    return render_template("index.html", mood=mood, weather=weather, mentioned=mentioned)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Nuh uh. Password or out.", 403)

        # Query database for username
        rows = db.execute("SELECT password FROM users WHERE user_id = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is not taken
        if len(rows) == 1:
            return apology("someone has already taken the same username", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        else:
            # https://www.w3schools.com/python/python_regex.asp
            pw = request.form.get("password")
            uppercase = re.search("[A-Z]", pw)
            lowercase = re.search("[a-z]", pw)
            number = re.search("[0-9]", pw)
            special_character = re.search("[@_!#$%^&*()<>?/\|}{~:]", pw)

            # Check password's criteria
            if not uppercase or not lowercase or not number or not special_character:
                return apology("password must contains alphanumeric and special characters", 400)

            # Make a new user
            else:
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                           request.form.get("username"), generate_password_hash(pw))

        return redirect("/")

    else:
        return render_template("register.html")

