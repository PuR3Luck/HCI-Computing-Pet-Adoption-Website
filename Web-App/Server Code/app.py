from flask import Flask, session, render_template, redirect, request 
import uuid
from werkzeug.datastructures import FileStorage
import sqlite3
from user_fns import login, register, change_password, delete_account, check_owner, check_interest, get_user_details
from pet_fns import add_pet, edit_pet, delete_pet
from search import search, filter_properties, convert_type_str_to_id, fetch
from interest_submission_fns import submit_interest, delete_interest, get_interests_in_pet
from view_interest import view_interest
from decorators import login_required, sql_wrapper
import base64
import io

app = Flask(__name__,template_folder='../templates', static_folder='../static')

# Generate secret key for session
SECRET_KEY = str(uuid.uuid1())
app.secret_key = SECRET_KEY

# Set up the database
@sql_wrapper
def setup_db(cursor: sqlite3.Cursor):
  cursor.execute("""CREATE TABLE IF NOT EXISTS PET (
              pet_id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_id INTEGER, name TEXT, age INTEGER, 
              fee FLOAT, 
              writeup TEXT, 
              sex TEXT, 
              type_id INTEGER, 
              FOREIGN KEY (user_id) REFERENCES USERS(user_id),
              FOREIGN KEY (type_id) REFERENCES TYPES(type_id)
              )""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS USER (
              user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT, 
              password TEXT, 
              contact_number INTEGER
              )""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS TYPES (
              type_id INTEGER PRIMARY KEY AUTOINCREMENT, 
              type TEXT
              )""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS INTERESTS (
              request_id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_id INTEGER, 
              pet_id INTEGER,
              FOREIGN KEY (user_id) REFERENCES USERS(user_id),
              FOREIGN KEY (pet_id) REFERENCES PET(pet_id)
              )""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS PET_PHOTOS (
              photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
              pet_id INTEGER,
              photo_blob BLOB,
              FOREIGN KEY (pet_id) REFERENCES PET(pet_id)
              )""")

  # Initialise type table
  if not cursor.execute("SELECT * FROM TYPES").fetchone(): # Make sure that the table is empty
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Dog",))
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Cat",))
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Bird",))
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Fish",))
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Reptile",))
    cursor.execute("INSERT INTO TYPES (type) VALUES (?)", ("Other",))

setup_db()

'''
if not cur.execute("SELECT * FROM USER").fetchall():
  cur.execute("INSERT INTO USER (username, password, contact_number) VALUES ('notbowen', 'root', '123456789');")
'''

@app.route('/', methods = ["GET"])
def landing_page():
  if session.get('logged_in'):
    return redirect("/home")
  
  else:
    return redirect("/login")
  
@app.route("/login", methods = ["GET", "POST"])
def login_page():
  if request.method == "GET":
    session['logged_in'] = False
    return render_template("login.html")
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    if login(username, password): # Successfully logged in
      session['logged_in'] = True
      
      con = sqlite3.connect('pets.db')
      cur = con.cursor()

      user_id = cur.execute("SELECT user_id FROM USER WHERE username =?", (username,)).fetchone()[0]
      username = cur.execute("SELECT username FROM USER WHERE username =?", (username,)).fetchone()[0]

      session['user_id'] = user_id
      session['username'] = username

      con.close()

      return redirect("/home")

    else:
      session['logged_in'] = False
      return render_template("login.html", error = "Invalid username or password")
    
@app.route("/register", methods = ["GET", "POST"])
def register_page():
  if request.method == "GET":
    return render_template("register.html")

  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    contact_number = request.form["contact_number"]

    try:
      contact_number = int(contact_number)
    except TypeError:
      return render_template("register.html", error = "Invalid contact number")

    if register(username, password, contact_number): # Successfully registered
      return redirect("/login")
    else:
      return render_template("register.html", error = "An error has occured")


@app.route("/home", methods = ["GET"]) # This is the home page
@login_required
def home_page():
  if request.method == "GET":
    user_pets_filter_properties = filter_properties(from_user = session.get("user_id"))

    user_pets = search(user_pets_filter_properties)

    list_of_pets = [fetch(pet_id) for pet_id in user_pets]

    return render_template("home.html", username = session.get("username"), pets = list_of_pets)

@app.route("/change_password", methods = ["GET", "POST"]) # This is the change password page
@login_required
def change_password_page():
  if request.method == "GET":
    return render_template("change_password.html")

  if request.method == "POST":
    prev_password = request.form["prev_password"]
    new_password = request.form["new_password"]

    if change_password(session.get("username"), prev_password, new_password):
      return render_template("success.html", message = "Password has been changed successfully")
    else:
      return render_template("error.html", error = "Invalid password")

@app.route("/delete_account", methods = ["GET", "POST"]) # This is the delete account page
@login_required
def delete_account_page():
  if request.method == "GET":
    return render_template("delete_account.html")
  
  if request.method == "POST":
    password = request.form["password"]

    if delete_account(session.get("username"), password):
      session.clear()
      return render_template("success.html", message = "Account has been successfully deleted")
    else:
      return render_template("error.html", error = "Invalid password")

@app.route("/add_pet", methods = ["GET", "POST"])
@login_required
def add_pet_page():

  if request.method == "GET":
    return render_template("add_pet.html")

  if request.method == "POST":
    name = request.form["name"]
    age = request.form["age"]
    fee = request.form["fee"]
    writeup = request.form["writeup"]
    sex = request.form["sex"]
    type = request.form["type"]

    type_id, _ = convert_type_str_to_id(type)

    photos_lst = request.files.getlist("photos")

    if add_pet(owner_id = session.get("user_id"), name = name, age = age, fee = fee, writeup = writeup, sex = sex, type_id = type_id, photos = photos_lst):
      return redirect("/home")
    else:
      return render_template("add_pet.html", error = "An error has occured")

@app.route("/edit_pet/<int:pet_id>", methods = ["GET", "POST"]) # This is the edit pet page
@login_required
def edit_pet_page(pet_id):
  if request.method == "GET":
    # Get pet properties
    pet_properties_result = fetch(pet_id)

    return render_template("edit_pet.html", pet_properties = pet_properties_result)


  if request.method == "POST":
    name = request.form["name"]
    age = request.form["age"]
    fee = request.form["fee"]
    writeup = request.form["writeup"]
    sex = request.form["sex"]
    type = request.form["type"]
    previous_photos = request.form.getlist("existing_photos")
    photos = request.files.getlist("photos")

    all_photos = []

    for photo in photos:
      if photo and photo.filename:
        all_photos.append(photo)

    for i, photo_base64 in enumerate(previous_photos):
      if photo_base64:
        photo_data = base64.b64decode(photo_base64)
        photo_file = io.BytesIO(photo_data)

        file_storage = FileStorage(
          stream=photo_file,
          filename=f'existing_photo_{i}.png',
          content_type='image/png'
        )

        all_photos.append(file_storage)

    photos = all_photos

    type_id = convert_type_str_to_id(type)[0]
    if edit_pet(pet_id, name, age, fee, writeup, sex, type_id, photos):
      return render_template("success.html", message="Successfully edited pet details")
    else:
      return render_template("error.html", error="Failed to edit pet")

@app.route("/delete_pet/<int:pet_id>", methods = ["GET", "POST"]) # This is the delete pet page
@login_required
def delete_pet_page(pet_id):
  if request.method == "GET":
    if delete_pet(pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Pet was not successfully deleted")
    
@app.route("/view_pet/<int:pet_id>", methods = ["GET"]) # This is the view pet page TODO
@login_required
def view_pet_page(pet_id):
  if request.method == "GET":
    pet_properties_result = fetch(pet_id)
    is_owner = check_owner(session["user_id"], pet_id)
    is_interested = check_interest(session["user_id"], pet_id)

    if is_owner:
      id_list, success = get_interests_in_pet(pet_id)
      print(id_list)
      if not success:
        return render_template("error.html", error = "An error has occured")
      
      detail_list = []

      for id in id_list:
        detail_list.append(get_user_details(id[0]))
      print(detail_list)
    else:
      detail_list = None
    
    return render_template("view_pet.html", pet_properties = pet_properties_result, is_owner = is_owner, is_interested = is_interested, detail_list = detail_list)

@app.route("/search", methods = ["GET", "POST"]) # This is the search page TODO
@login_required
def search_page():
  if request.method == "GET":
    return render_template("search.html")
  
  if request.method == "POST":
    search_properties =  filter_properties(
      min_age = request.form["min_age"],
      max_age = request.form["max_age"],
      min_fee = request.form["min_fee"],
      max_fee = request.form["max_fee"],
      sex = request.form["sex"],
      type = request.form["type"]
    )

    search_results = search(search_properties)

    return render_template("search.html", pets = search_results)

@app.route("/submit_interest/<int:pet_id>", methods = ["GET"]) # This is the submit interest page TODO
@login_required
def submit_interest_page(pet_id):
  if request.method == "GET":
    if submit_interest(session.get("user_id"), pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Interest was not successfully registered")

@app.route("/delete_interest/<int:pet_id>", methods = ["GET"]) # This is the delete interest page TODO
@login_required
def delete_interest_page(pet_id):
  if request.method == "GET":
    if delete_interest(session.get("user_id"), pet_id):
      return redirect("/home")
    else:
      return render_template("error.html", error = "Interest was not successfully deleted")

@app.route("/test_error", methods = ["GET"]) # This is the test error page
def test_error_page():
  return render_template("error.html", error = "This is a test error page")

if __name__ == "__main__":
  app.run(debug=True)