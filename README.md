# LUCISCO - DAILY JOURNEY

## Video Demo: <URL HERE>

---

## Description:

### About

<div ctyle="text-align: justify">

A simple web based application to write some important things or a journal daily focusing on simplicity with autosave function.

</div>

### Background Story

<div style="text-align: justify">

At first, I was about to make something similar, more to daily task in mobile phone, yet... let's say some people have a tendency to ignore the plans. So, rather than planning, I think it is better to see what we have accomplished in daily basis and and compare the results to see our own progresses.

Another personal reason is, I used to keep simple journal on my NDS as a habit from more than a decade ago. It is easy to use yet the date stopped adding after year 2020.

The last reason of this is to try implementing what I have learnt about Python Flask. I am planning to continuously explore this in the future; including but not limited to graphical analysis (well, once I get the hang of machine learning which theories are the only one with me right now...)

</div>

---

## Design:

### Name

The simple, to the point of the application's name itself is "Daily Journey", then I decided to add it to a (maybe) serie named "Lucisco", in which I would use to learn things. Lucisco is taken from Latin, which meaning is "Dawn".

>

The simple philosophy behind it is to continue rising like a new day.

### Logo

<div style="text-align: justify">

Continueing from the name, the first thing that came to my mind about "continue rising" is a phoenix, for some reasons I refuse to indulge. Nuh uh. Emotions go bye-bye. Anyway, so I made the logo of Lucisco as a phoenix.

</div>

### Color

<div style="text-align: justify">

Dawn's and phoenix's colors are of course, shades of beautiful red, but nah, let's be the weird one. I choose blue for the brand's color is to convey calmness when facing problems even if some parts of us might be burning with uncontrollable enerby.

</div>

---

## Database

[image]

From the ERD, we could get tables:

1. beverages

This table contains the list of beverages that each user can modified according to their own habits.

2. daily_beverages

This table contains the list of beverages a user consumes per day. In the beginning, I consider only adding a number of glasses, but some people like to control their sugar intake or other stuff.

3. daily_food

This table is the list of food a user consumes per day.

4. expenses

This table contains daily transactions, not just expenses, though it is named like that since most people are more familiar with it.

5. food

This table contains the list of food that each user can modified according to their own habits.

6. importances

This section of database contains list of important stuff, anything, that present at the day.

7. journey

This table is the main journey data.

8. moods

This table contains the list of moods that each user can modified according to their own... usual emotional range.

9. people

Now, this is the feature that I firstly (and never again) found in the said NDS game; a section to input a person per day. The context of it, I leave it to you to interprete, whether the most favorite person, the one brings you happiness, the one ruins your day, or the one you dayream about :D

10. users

At first, I want to make it either userless or just a simple user with a single password, but considering there would be some people using the same device together or even some snoppers snooping around, I decided to make it multiusers anyway.

11. weathers

This table contains daily most weather. Yeah, most. Just one per day.

---

## Structures

### folders

- additionals
- static
- templates

### Other Files

- app.py
- daily-journey.sql
- helpers.py
- README.md

---

## Project setup

### Dependencies

- pip install Flask
- pip install flask-mysql
- pip install flask_session
- pip install requests
- pip install flask_mail
- pip install waitress
- pip install flask_mysqldb

### Starting

- python3 -m venv venv
- venv\Scripts\activate
- flask run

### If something goes wrong

- export FLASK_APP=app

---

## References and Credits

### Images Source

- Logo Image

Phoenix
By		: Saeful Muslim
Source	: The Noun Project
License	: CC BY
Link    : <a href="https://thenounproject.com/icon/phoenix-2266436/">Phonix icon</a>

### UI/UX Inspiration

<a href="https://dribbble.com/tags/notes_app">Notes app</a> in <a href="https://dribbble.com">Dribbble</a>

### Codes Reference



### Tools Used

Visual Studio Code

- To build

Figma

- To edit logo
- UI/UX

Adobe Creative Cloud Express

- To make logo

### Other references for reminder

- <a href="https://flask-mysql.readthedocs.io/en/stable/">Setting up flask with MySQL</a>
- <a href="https://tableplus.com/blog/2018/09/ms-sql-server-how-to-get-date-only-from-datetime-value.html">Converting current time into desired value and format</a>
