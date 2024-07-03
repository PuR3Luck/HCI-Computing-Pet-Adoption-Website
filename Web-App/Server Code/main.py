import flask
from flask import Flask, session, render_template, redirect, request, url_for
import uuid
from werkzeug.utils import secure_filename
import sqlite3
from user_fns import login, register, change_password, delete_account
from pet_fns import add_pet, edit_pet, delete_pet
from search import search
from interest_submission_fns import submit_interest, delete_interest
from view_interest import view_interest

app = Flask(__name__)


# Set up the database
con = sqlite3.connect('pets.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS PETS (pet_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER FOREIGN KEY, name TEXT, age INTEGER, fee FLOAT, writeup TEXT, sex TEXT, type_id INTEGER FOREIGN KEY, photos BLOB)")
cur.execute("CREATE TABLE IF NOT EXISTS USERS (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, contact_number INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS TYPES (type_id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS INTERESTS (request_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER FOREIGN KEY, pet_id INTEGER FOREIGN KEY)")
con.commit()
con.close()

# Set up the flask session
session.get('logged_in', False)


@app.route('/', methods = ["GET"]) # This is the home page
def landing_page():
  if flask.session.get('logged_in'):
    return redirect("/home")
  
  else:
    return redirect("/login")
  
@app.route("/login", methods = ["GET", "POST"]) # This is the login page
def login_page():
  if request.method == "GET":
    return render_template("login.html")
  
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    if login(username, password): # Successfully logged in
      session['logged_in'] = True
      
      con = sqlite3.connect('pets.db')
      cur = con.cursor()

      user_id = cur.execute("SELECT user_id FROM USERS WHERE username =?", (username,)).fetchone()[0]

      session['user_id'] = user_id

      con.close()

      return redirect("/home")

    else:
      return render_template("login.html", error = "Invalid username or password")
    
@app.route("/register", methods = ["GET", "POST"]) # This is the register page

@app.route("/home", methods = ["GET", "POST"]) # This is the home page NOTE: Should have top-k interests here

@app.route("/change_password", methods = ["GET", "POST"]) # This is the change password page

@app.route("/delete_account", methods = ["GET", "POST"]) # This is the delete account page

@app.route("/add_pet", methods = ["GET", "POST"]) # This is the add pet page

@app.route("/edit_pet", methods = ["GET", "POST"]) # This is the edit pet page

@app.route("/delete_pet", methods = ["GET", "POST"]) # This is the delete pet page

@app.route("/search", methods = ["GET", "POST"]) # This is the search page

@app.route("/submit_interest", methods = ["GET", "POST"]) # This is the submit interest page

@app.route("/delete_interest", methods = ["GET", "POST"]) # This is the delete interest page

@app.route("/view_interest", methods = ["GET", "POST"]) # This is the view interest page









if __name__ == "__main__":
  app.run(debug=True)