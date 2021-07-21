from recipes_app import app
from flask import render_template, request, redirect, session
# from recipes_app.models import user
from recipes_app.models import recipe
from recipes_app.controllers import users

# shows the information of one recipe
@app.route('/recipes/<int:recipe_id>')
def show_one_recipe(recipe_id):
  if users.user_logged_in() == False:
    return redirect('/')
  else:
    logged_in_user = users.user_logged_in() 
  
  # if user is logged in
  recipe_data = {
    "recipe_id": recipe_id
  }
  one_recipe = recipe.Recipe.get_one(recipe_data)

  # instructions separated by .
  recipe_instructions = one_recipe['instructions'].split('.')
  return render_template("one_recipe.html", logged_in_user=logged_in_user, one_recipe=one_recipe, recipe_instructions=recipe_instructions)

# Allow users to add a new recipe
@app.route('/recipes/new')
def create_recipe():
  # only allow logged in users to add new recipe
  if users.user_logged_in() == False:
    return redirect('/')
  else:
    logged_in_user = users.user_logged_in() 
  
  # if user is logged in
  return render_template("new_recipe.html", logged_in_user=logged_in_user)

# Takes user input and add it to recipe database
@app.route('/add/recipe', methods=["POST"])
def add_recipe():
  # validate input
  if not recipe.Recipe.validate_recipe(request.form):
    return redirect('/recipes/new')
  
  # if input is valid
  recipe_data = {
    "name": request.form["name"],
    "description": request.form["description"], 
    "under_30_mins": request.form["under_30_mins"],
    "instructions": request.form["instructions"],
    "user_id": session["user_id"],
    "created_at": request.form["created_at"]
  }

  recipe_id = recipe.Recipe.save(recipe_data)
  return redirect(f'/dashboard')

# Page to edit recipe
@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe_page(recipe_id):
  # only allow logged in users to edit recipes
  if users.user_logged_in() == False:
    return redirect('/')
  
  # if user is logged in, check if user is creator of recipe
  recipe_user_id = recipe.Recipe.get_one({"recipe_id": recipe_id})['user_id']

  if recipe_user_id != session["user_id"]:
    return redirect("/dashboard")

  # if user is logged in and creator of recipe
  recipe_data = recipe.Recipe.get_one({"recipe_id": recipe_id})
  return render_template("edit.html", recipe=recipe_data)

# update recipe based on user input
@app.route('/edit/recipe/<int:recipe_id>', methods=["POST"])
def edit_recipe(recipe_id):
  # validate input
  if not recipe.Recipe.validate_recipe(request.form):
    return redirect(f'/recipes/edit/{recipe_id}')
  
  # if input is valid
  recipe_data = {
    "id": recipe_id,
    "name": request.form["name"],
    "description": request.form["description"], 
    "under_30_mins": request.form["under_30_mins"],
    "instructions": request.form["instructions"],
    "user_id": session["user_id"],
    "created_at": request.form["created_at"]
  }

  recipe.Recipe.update_recipe(recipe_data)
  return redirect(f'/dashboard')

# delete recipe
@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
  # only allow logged in users to edit recipes
  if users.user_logged_in() == False:
    return redirect('/')

  # if user is logged in, check if user is creator of recipe
  recipe_user_id = recipe.Recipe.get_one({"recipe_id": recipe_id})['user_id']

  if recipe_user_id != session["user_id"]:
    return redirect("/dashboard")
  

  # if user is creator of recipe and logged in
  recipe.Recipe.delete({"recipe_id": recipe_id})
  return redirect('/dashboard')
