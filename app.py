import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

import re
from datetime import datetime

from helpers import apology, login_required

app = Flask(__name__)

# Ensure templates auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Session uses filesystem, not signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'daily-journey'

mysql = MySQL(app)


@app.after_request
def after_request(response):
    """responses are not cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# KAEYA
@app.route("/")
@login_required
def index():
    """Show locked page"""
    # Gets data from database
    cursor = mysql.connection.cursor()
    j = cursor.execute("SELECT * FROM journeys WHERE date = (SELECT CONVERT(VARCHAR(10), GETDATE(), 105)) AND username = ?", session["username"])
    journey = j[0]["journey"]
    m = cursor.execute("SELECT AVERAGE(mood) AS mood FROM general WHERE username = ? GROUP BY username", session["username"])
    w = cursor.execute("SELECT COUNTA(weather) AS weather FROM general WHERE username = ? GROUP BY username", session["username"])
    p = cursor.execute("SELECT COUNTA(mentioned) AS person FROM general WHERE username = ? GROUP BY username", session["username"])

    # If there is no data yet
    if len(m) >= 1:
        mood = m[0]["mood"]
        weather = w[0]["weather"]
        mentioned = p[0]["mentioned"]
    else:
        mood = 0
        weather = "None"
        mentioned = "Nobody :( are you lonely?"

    cursor.close()

    return render_template("index.html", mood=mood, weather=weather, mentioned=mentioned)


@app.route("/login", methods=["GET", "POST"])
def login():
    """log user in"""

    # Forget any username
    session.clear()

    # If submitting a form
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        # Query database for username
        rows = cursor.execute("SELECT password FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["username"] = rows[0]["username"]
        cursor.close()

        # Redirect user to home page
        return redirect("/")

    # If going to page
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any username
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

        cursor = mysql.connection.cursor()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
                cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                           request.form.get("username"), generate_password_hash(pw))
        
        cursor.close()
        return redirect("/")

    else:
        return render_template("register.html")

