from flask import Flask, redirect, flash, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
from datetime import datetime

import re

from helpers import login_required


app = Flask(__name__)

# Ensure templates auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Session uses filesystem, not signed cookies
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database; this is the default, configure it to suit your own
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'daily-journey'

mysql = MySQL(app)


@app.after_request
def after_request(response):
    """
    CS50 PSET 9; with staff's solution as reference
    """
    # Responses are not cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (session["user_id"], ))
    user = cursor.fetchone()
    cursor.execute("SELECT j.id, j.user_id, j.mood_id, m.name, j.weather_id, w.name, j.person_id, p.name, j.date, j.title, j.diary FROM journeys j JOIN moods m ON(j.mood_id = m.id) JOIN weathers w ON(j.weather_id = w.id) JOIN people p ON(j.person_id = p.id) WHERE j.user_id LIKE %s", (session["user_id"], ))
    journeys = cursor.fetchall()
    cursor.close()

    return render_template("index.html", user=user, journeys=journeys)


@app.route("/journeys/create", methods=['GET', 'POST'])
def add_journey():
    cursor = mysql.connection.cursor()
    user_id = session["user_id"]

    if request.method == "POST":
        mood_id = request.form['mood_id']
        weather_id = request.form['weather_id']
        person_id = request.form['person_id']
        date = request.form['date']
        title = request.form['title']
        diary = request.form['diary']

        cursor.execute("INSERT INTO journeys (user_id, mood_id, weather_id, person_id, date, title, diary) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, mood_id, weather_id, person_id, date, title, diary))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('index'))

    else:
        cursor.execute("SELECT * FROM moods WHERE user_id LIKE %s", (user_id, ))
        moods = cursor.fetchall()
        cursor.execute("SELECT * FROM weathers WHERE user_id LIKE %s", (user_id, ))
        weathers = cursor.fetchall()
        cursor.execute("SELECT * FROM people WHERE user_id LIKE %s", (user_id, ))
        people = cursor.fetchall()

        return render_template('journeys/create.html', moods=moods, weathers=weathers, people=people)


@app.route('/journeys/edit/<int:id>', methods=['GET', 'POST'])
def edit_journey(id):
    if request.method == "POST":
        mood_id = request.form['mood_id']
        weather_id = request.form['weather_id']
        person_id = request.form['person_id']
        date = request.form['date']
        title = request.form['title']
        diary = request.form['diary']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE journeys SET mood_id = %s, weather_id = %s, person_id = %s, date = %s, title = %s, diary = %s WHERE id = %s", (mood_id, weather_id, person_id, date, title, diary, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('journeys'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM journeys WHERE id = %s", (id, ))
        journey = cursor.fetchone()
        cursor.close()

        return render_template('journeys/edit.html', journey=journey)


@app.route('/journeys/delete/<int:id>', methods=['GET'])
def delete_journey(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM expenses WHERE journey_id LIKE %s", (id, ))
        mysql.connection.commit()
        cursor.execute("DELETE FROM importances WHERE journey_id LIKE %s", (id, ))
        mysql.connection.commit()
        cursor.execute("DELETE FROM food WHERE journey_id LIKE %s", (id, ))
        mysql.connection.commit()
        cursor.execute("DELETE FROM beverages WHERE journey_id LIKE %s", (id, ))
        mysql.connection.commit()
        cursor.execute("DELETE FROM journeys WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('journeys'))

    else:
        return render_template('journeys.html')


@app.route('/journeys/edit/<int:journey_id>/importances/create', methods=['GET', 'POST'])
def add_importance(journey_id):
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO importances (user_id, journey_id, name, notes) VALUES (%s, %s, %s, %s)", (user_id, journey_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('journeys'))

    else:
        return render_template('importances/create.html')


@app.route('/journeys/edit/<int:journey_id>/importances/edit/<int:id>', methods=['GET', 'POST'])
def edit_importance(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE importances SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('weathers'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM importances WHERE id = %s", (id, ))
        importance = cursor.fetchone()
        cursor.close()

        return render_template('importances/edit.html', importance=importance)


@app.route('/journeys/edit/<int:journey_id>/importances/delete/<int:id>', methods=['GET', 'POST'])
def delete_importance(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM importances WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('joureys'))

    else:
        return render_template('journeys.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget user
    session.clear()

    # If submitting a form
    if request.method == "POST":
        # Get data from database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form["username"], ))
        rows = cursor.fetchone()

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[2], request.form["password"]):
            return render_template("apology.html", message="Invalid username and/or password.")

        # Remember user
        session["user_id"] = rows[0]
        # Close db
        cursor.close()

        # Redirect to index/login
        return redirect("/")

    # If going to page
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        cursor = mysql.connection.cursor()
        un = request.form["un"]
        pw = request.form['pw']
        cursor.execute("SELECT username FROM users WHERE username = %s", (un, ))
        rows = cursor.fetchone()

        # Ensure unique username
        if rows:
            return render_template("apology.html", message="Someone has already taken the same username :(")

        # Ensure password and confirmation match
        elif pw != request.form['confirm']:
            return render_template("apology.html", message="Passwords do not match.")

        else:
            # Password criterias: one uppercase, one lowercase, one number, one special character
            uppercase = re.search("[A-Z]", pw)
            lowercase = re.search("[a-z]", pw)
            number = re.search("[0-9]", pw)
            special_character = re.search("[@_!#$%^&*()<>?/\|}{~:]", pw)

            # Check password's criterias
            if not uppercase or not lowercase or not number or not special_character:
                return render_template("apology.html", message="Password must contains at least one uppercase and lowercase alphanumeric with one special character.")

            # Make a new user
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (un, generate_password_hash(pw)))
                mysql.connection.commit()

        cursor.close()

        return redirect("/")

    else:
        return render_template("login.html")


@app.route('/beverages')
def beverages():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM beverages where user_id LIKE %s", (session["user_id"], ))
    beverages = cursor.fetchall()
    cursor.close()

    return render_template('beverages/index.html', beverages=beverages)


@app.route('/beverages/create', methods=['GET', 'POST'])
def add_beverage():
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO beverages (user_id, name, notes) VALUES (%s, %s, %s)", (user_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('beverages'))

    else:
        return render_template('beverages/create.html')


@app.route('/beverages/edit/<int:id>', methods=['GET', 'POST'])
def edit_beverage(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE beverages SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('beverages'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM beverages WHERE id = %s", (id, ))
        beverage = cursor.fetchone()
        cursor.close()

        return render_template('beverages/edit.html', beverage=beverage)


@app.route('/beverages/delete/<int:id>', methods=['GET'])
def delete_beverage(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM beverages WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('beverages'))

    else:
        return render_template('beverages.html')


@app.route('/food')
def food():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM food where user_id LIKE %s", (session["user_id"], ))
    food = cursor.fetchall()
    cursor.close()

    return render_template('food/index.html', food=food)


@app.route('/food/create', methods=['GET', 'POST'])
def add_food():
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO food (user_id, name, notes) VALUES (%s, %s, %s)", (user_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('food'))

    else:
        return render_template('food/create.html')


@app.route('/food/edit/<int:id>', methods=['GET', 'POST'])
def edit_food(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE food SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('food'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM food WHERE id = %s", (id, ))
        food = cursor.fetchone()
        cursor.close()

        return render_template('food/edit.html', food=food)


@app.route('/food/delete/<int:id>', methods=['GET'])
def delete_food(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM food WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('food'))

    else:
        return render_template('food.html')


@app.route('/moods')
def moods():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM moods where user_id LIKE %s", (session["user_id"], ))
    moods = cursor.fetchall()
    cursor.close()

    return render_template('moods/index.html', moods=moods)


@app.route('/moods/create', methods=['GET', 'POST'])
def add_mood():
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO moods (user_id, name, notes) VALUES (%s, %s, %s)", (user_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('moods'))

    else:
        return render_template('moods/create.html')


@app.route('/moods/edit/<int:id>', methods=['GET', 'POST'])
def edit_mood(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE moods SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('moods'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM moods WHERE id = %s", (id, ))
        beverage = cursor.fetchone()
        cursor.close()

        return render_template('moods/edit.html', beverage=beverage)


@app.route('/moods/delete/<int:id>', methods=['GET'])
def delete_mood(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM moods WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('moods'))

    else:
        return render_template('moods.html')


@app.route('/people')
def people():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM people where user_id LIKE %s", (session["user_id"], ))
    people = cursor.fetchall()
    cursor.close()

    return render_template('people/index.html', people=people)


@app.route('/people/create', methods=['GET', 'POST'])
def add_person():
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO people (user_id, name, notes) VALUES (%s, %s, %s)", (user_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('people'))

    else:
        return render_template('people/create.html')


@app.route('/people/edit/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE people SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('people'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM people WHERE id = %s", (id, ))
        beverage = cursor.fetchone()
        cursor.close()

        return render_template('people/edit.html', beverage=beverage)


@app.route('/people/delete/<int:id>', methods=['GET'])
def delete_person(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM people WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('people'))

    else:
        return render_template('people.html')


@app.route('/weathers')
def weathers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM weathers where user_id LIKE %s", (session["user_id"], ))
    weathers = cursor.fetchall()
    cursor.close()

    return render_template('weathers/index.html', weathers=weathers)


@app.route('/weathers/create', methods=['GET', 'POST'])
def add_weather():
    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO weathers (user_id, name, notes) VALUES (%s, %s, %s)", (user_id, name, notes))
        mysql.connection.commit()
        cursor.close()

        flash("Data added.", "success")
        return redirect(url_for('weathers'))

    else:
        return render_template('weathers/create.html')


@app.route('/weathers/edit/<int:id>', methods=['GET', 'POST'])
def edit_weather(id):
    if request.method == "POST":
        name = request.form['name']
        notes = request.form['notes']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE weathers SET name = %s, notes = %s WHERE id = %s", (name, notes, id))
        mysql.connection.commit()
        cursor.close()

        flash("Data edited.", "success")
        return redirect(url_for('weathers'))

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM weathers WHERE id = %s", (id, ))
        beverage = cursor.fetchone()
        cursor.close()

        return render_template('weathers/edit.html', beverage=beverage)


@app.route('/weathers/delete/<int:id>', methods=['GET'])
def delete_weather(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM weathers WHERE id = %s", (id, ))
        mysql.connection.commit()
        cursor.close()

        flash("Data deleted", "success")
        return redirect(url_for('weathers'))

    else:
        return render_template('weathers.html')
