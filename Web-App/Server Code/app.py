import flask
from flask import Flask, session, render_template, redirect, request, url_for
import uuid
from werkzeug.utils import secure_filename
import sqlite3
from user_fns import login, register, change_password, delete_account
from pet_fns import add_pet, edit_pet, delete_pet
from search import search, filter_properties, convert_type_str_to_id
from interest_submission_fns import submit_interest, delete_interest
from view_interest import view_interest

app = Flask(__name__)


# Set up the database
con = sqlite3.connect('pets.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS PETS (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, name TEXT, age INTEGER, 
            fee FLOAT, 
            writeup TEXT, 
            sex TEXT, 
            type_id INTEGER, 
            photos BLOB,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id),
            FOREIGN KEY (type_id) REFERENCES TYPES(type_id)
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS USER (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            password TEXT, 
            contact_number INTEGER
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS TYPES (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            type TEXT
            )""")

cur.execute("""CREATE TABLE IF NOT EXISTS INTERESTS (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            pet_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id),
            FOREIGN KEY (pet_id) REFERENCES PETS(pet_id)
            )""")

# Initialise type table
if not cur.execute("SELECT * FROM TYPES").fetchone(): # Make sure that the table is empty
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Dog",))
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Cat",))
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Bird",))
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Fish",))
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Reptile",))
  cur.execute("INSERT INTO TYPES (type) VALUES (?)", ("Other",))

con.commit()
con.close()

# Set up the flask session
session.get('logged_in', False)


@app.route('/', methods = ["GET"]) # This is the home page
def landing_page():
  if session.get('logged_in'):
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
      username = cur.execute("SELECT username FROM USERS WHERE username =?", (username,)).fetchone()[0]

      session['user_id'] = user_id
      session['username'] = username

      con.close()

      return redirect("/home")

    else:
      return render_template("login.html", error = "Invalid username or password")
    
@app.route("/register", methods = ["GET", "POST"]) # This is the register page
def register_page():
  if request.method == "GET":
    return render_template("register.html")

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    contact_number = request.form["contact_number"]

    if register(username, password, contact_number): # Successfully registered
      return redirect("/login")
    else:
      return render_template("register.html", error = "Username already exists")


@app.route("/home", methods = ["GET"]) # This is the home page NOTE: Should show all pets
def home_page():
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    user_pets_filter_properties = filter_properties(from_users = [session.get("user_id")])

    user_pets = search(user_pets_filter_properties)

    return render_template("home.html", pets = user_pets)

@app.route("/change_password", methods = ["GET", "POST"]) # This is the change password page
def change_password_page():
  if not session.get("logged_in"):
    return redirect("/login")

  if request.method == "GET":
    return render_template("change_password.html")

  if request.method == "POST":
    prev_password = request.form["prev_password"]
    new_password = request.form["new_password"]

    if change_password(session.get("username"), prev_password, new_password):
      return redirect("/successful_password_change")
    else:
      return render_template("change_password.html", error = "Invalid password")

@app.route("/delete_account", methods = ["GET", "POST"]) # This is the delete account page
def delete_account_page():
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    return render_template("delete_account.html")
  
  if request.method == "POST":
    password = request.form["password"]

    if delete_account(session.get("username"), password):
      session.clear()
      return redirect("/successful_account_deletion")
    else:
      return render_template("delete_account.html", error = "Invalid password")

@app.route("/add_pet", methods = ["GET", "POST"]) # This is the add pet page
def add_pet_page(): # NOTE: TO-DO
  raise NotImplementedError
  if not session.get("logged_in"):
    return redirect("/login")

  if request.method == "GET":
    return render_template("add_pet.html")

  if request.method == "POST":
    name = request.form["name"]
    age = request.form["age"]
    fee = request.form["fee"]
    writeup = request.form["writeup"]
    sex = request.form["sex"]
    type = request.form["type"]

    type_id = convert_type_str_to_id(type)

    photos_lst = request.files

    # Save photos in blob


    if add_pet(owner_id = session.get("user_id"), name = name, age = age, fee = fee, writeup = writeup, sex = sex, type = type_id, photos = photos_lst):
      return render_template("successful_pet_addition.html")


@app.route("/edit_pet", methods = ["GET", "POST"]) # This is the edit pet page
def edit_pet_page(pet_id): #NOTE: Check for how to handle photos
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    # Get pet properties
    con = sqlite3.connect('pets.db')
    cur = con.cursor()
    pet_properties = cur.execute("SELECT * FROM PETS WHERE pet_id = ?", (pet_id,)).fetchone()[0] 
    con.close()

    # Convert a tuple into a list
    pet_properties_list = list(pet_properties)
    web_pet_properties = pet_properties_list[2:-1]

    return render_template("edit_pet.html", pet_properties = web_pet_properties)


  if request.method == "POST":
    name = request.form["name"]
    age = request.form["age"]
    fee = request.form["fee"]
    writeup = request.form["writeup"]
    sex = request.form["sex"]
    type = request.form["type"]
    photos = request.files
    type_id = convert_type_str_to_id(type)
    if edit_pet(pet_id, name, age, fee, writeup, sex, type_id, photos):
      return redirect("/home")
    else:
      return render_template("error.html", error="Failed to edit pet")

@app.route("/delete_pet", methods = ["GET", "POST"]) # This is the delete pet page
def delete_pet_page(pet_id):
  if not session.get("logged_in"):
    return redirect("/login")

  if request.method == "GET":
    if delete_pet(pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Invalid pet id")

@app.route("/search", methods = ["GET", "POST"]) # This is the search page
def search_page():
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    return render_template("search.html")
  
  if request.method == "POST":
    search_properties =  filter_properties(
      from_users = [request.form["from_users"]],
      min_age = request.form["min_age"],
      max_age = request.form["max_age"],
      min_fee = request.form["min_fee"],
      max_fee = request.form["max_fee"],
      sex = request.form["sex"],
      type = request.form["type"]
    )

    search_results = search(search_properties)

    return render_template("search.html", pets = search_results)

@app.route("/submit_interest", methods = ["GET", "POST"]) # This is the submit interest page
def submit_interest_page(pet_id):
  if not session.get("logged_in"):
    return redirect("/login")

  if request.method == "GET":
    if submit_interest( session.get("user_id"), pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Invalid pet id")

@app.route("/delete_interest", methods = ["GET", "POST"]) # This is the delete interest page
def delete_interest_page(pet_id):
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    if delete_interest(session.get("user_id"), pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Invalid pet id")

@app.route("/view_interest_pet", methods = ["GET"]) # This is the view interest page
def view_interest_page(pet_id):
  if not session.get("logged_in"):
    return redirect("/login")
  
  if request.method == "GET":
    interests = view_interest(pet_id)
    return render_template("view_interest.html", interests = interests)


if __name__ == "__main__":
  app.run(debug=True)