from recipes_app import app
from flask import render_template, request, redirect, session
from recipes_app.models import user
from recipes_app.models import recipe
import datetime, math

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# this function returns the user if user is logged in and exists in our database,
# else redirects and return false
# def user_logged_in():
#   # if no user logged in, redirect to login/registration page
#   if "user_id" not in session:
#     return False

#   data = {
#     "user_id" : session["user_id"]
#   }

#   logged_in_user = user.User.get_user_by_id(data)

#   # # if somehow managed to have user id in session but not in our database
#   # if logged_in_user == False:
#   #   return False
  
#   # # if user logged in
#   # return logged_in_user

@app.route('/')
def index():
  if "user_id" in session:
    return redirect('/dashboard')
  return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
  # if there are errors:
  # We call the staticmethod on User model to validate
  if not user.User.validate_registration(request.form):
    return redirect('/')
  pw_hash = bcrypt.generate_password_hash(request.form['password'])
  data = {
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": pw_hash,
  }
  user_id = user.User.save(data)
  # session.clear() # can remove if we don't plan to store half-registered data
  session['user_id'] = user_id
  return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # validate if login information matches
    data = { 
      "email" : request.form["email_login"],
      "password": request.form["pw_login"]
    }
    validate_login = user.User.validate_login(data)
    if not validate_login:
      return redirect('/')

    # if the passwords matched, we set the user_id into session
    session['user_id'] = validate_login.id
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
  # if no user logged in, redirect to login/registration page
  if "user_id" not in session:
    return redirect('/')

  data = {
    "user_id" : session["user_id"]
  }

  logged_in_user = user.User.get_user_by_id(data)

  # get all recipes
  all_recipes = recipe.Recipe.get_all()
  # if user is logged in, return to wall page
  return render_template("dashboard.html", logged_in_user = logged_in_user, all_recipes = all_recipes)


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')




