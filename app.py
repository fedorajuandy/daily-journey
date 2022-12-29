from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL

import re
from datetime import datetime

from helpers import login_required

app = Flask(__name__)

# Ensure templates auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Session uses filesystem, not signed cookies
app.config["SESSION_FILE_DIR"] = mkdtemp()
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
    # Responses are not cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("journey.html")

    # Get data from database
    """ cursor = mysql.connection.cursor()
    j = cursor.execute("SELECT * FROM journeys WHERE date = (SELECT CONVERT(VARCHAR(10), GETDATE(), 105)) AND username = ?", session["username"])
    journey = j[0]["journey"]
    m = cursor.execute("SELECT AVERAGE(mood) AS mood FROM general WHERE username = ? GROUP BY username", session["username"])
    w = cursor.execute("SELECT COUNTA(weather) AS weather FROM general WHERE username = ? GROUP BY username", session["username"])
    p = cursor.execute("SELECT COUNTA(mentioned) AS person FROM general WHERE username = ? GROUP BY username", session["username"])

    # If there is no data yet
    if m >= 1:
        mood = m[0]["mood"]
        weather = w[0]["weather"]
        mentioned = p[0]["mentioned"]
    else:
        mood = 0
        weather = "None"
        mentioned = "Nobody :( are you lonely?"

    cursor.close() """



@app.route("/login", methods=["GET", "POST"])
def login():
    """log user in"""

    # Forget any username
    session.clear()

    # If submitting a form
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form["username"], ))
        rows = cursor.fetchone()

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[2], request.form["password"]):
            return render_template("apology.html", message="Invalid username and/or password")

        # Remember which user has logged in
        session["username"] = rows[1]
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
        cursor = mysql.connection.cursor()
        un = request.form["un"]
        pw = request.form['pw']
        cursor.execute("SELECT username FROM users WHERE username = %s", (un, ))
        rows = cursor.fetchone()

        """ Ensure username is not taken """
        if rows:
            return render_template("apology.html", message="Someone has already taken the same username")

        elif pw != request.form['confirm']:
            """ Ensure passwords match """
            return render_template("apology.html", message="Passwords don't match")

        else:
            """ https://www.w3schools.com/python/python_regex.asp """
            uppercase = re.search("[A-Z]", pw)
            lowercase = re.search("[a-z]", pw)
            number = re.search("[0-9]", pw)
            special_character = re.search("[@_!#$%^&*()<>?/\|}{~:]", pw)

            # Check password's criteria
            if not uppercase or not lowercase or not number or not special_character:
                return render_template("apology.html", message="Password must contains alphanumeric and special characters")

            # Make a new user
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (un, generate_password_hash(pw)))
                mysql.connection.commit()

        cursor.close()
        return redirect("/")

    else:
        return render_template("login.html")
