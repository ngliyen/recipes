# import the function that will return an instance of a connection
from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
  def __init__(self,data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.under_30_mins = data['under_30_mins']
    self.instructions = data['instructions']
    self.user_id = data['user_id']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM recipes;"
    # call connectToMySQL function with the schema
    results = connectToMySQL('recipes').query_db(query)
    # create an empty list to store all instances of users
    recipes = []
    # iterate over the db results and create instances of users with cls
    for recipe in results:
      recipes.append( cls(recipe) )
    return recipes

  @classmethod
  def get_one(cls, data):
    query = "SELECT * FROM recipes WHERE id= %(recipe_id)s ;"
    results = connectToMySQL('recipes').query_db(query, data)
    if len(results) > 0:
      # return results[0]
      return cls(results[0])
    else:
      return False

  @classmethod
  def save(cls, data):
    query = "INSERT INTO recipes (name, description, under_30_mins, instructions, user_id, created_at, updated_at) VALUES ( %(name)s,%(description)s,%(under_30_mins)s,%(instructions)s,%(user_id)s,%(created_at)s, NOW() );"
    return connectToMySQL('recipes').query_db(query, data)

  @classmethod
  def update_recipe(cls, data):
    query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_mins = %(under_30_mins)s, instructions = %(instructions)s, user_id = %(user_id)s, created_at = %(created_at)s, updated_at = NOW() WHERE id = %(id)s;"
    return connectToMySQL('recipes').query_db( query, data )

  @classmethod
  def delete(cls,data):
    query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
    return connectToMySQL('recipes').query_db(query, data)

  # @classmethod
  # def num_messages_by_user(cls,data):
  #   query = "SELECT * FROM messages where messages.user_id = %(user_id)s;"
  #   results = connectToMySQL('private_wall').query_db(query, data)
  #   print(len(results))
  #   return len(results)


  @staticmethod
  def validate_recipe(recipe_data):
    is_valid = True

    # name
    # make sure it is not an empty string
    if len(recipe_data['name']) == 0:
      flash("Recipe name is required.", "name")
      is_valid = False
    # check that there's at least 3 characters
    elif len(recipe_data['name']) < 3:
      flash("Recipe name must have at least 3 characters.", "name")
      is_valid = False

    # description
    # make sure it is not an empty string
    if len(recipe_data['description']) == 0:
      flash("Recipe description is required.", "description")
      is_valid = False
    # check that there's at least 3 characters
    elif len(recipe_data['description']) < 3:
      flash("Recipe description must have at least 3 characters.", "description")
      is_valid = False
    # check that it's not more than 255 characters (set varchar(255) in database)
    elif len(recipe_data['description']) > 255:
      flash("Recipe description must be less than 255 characters.", "description")
      is_valid = False

    # instructions
    # make sure it is not an empty string
    if len(recipe_data['instructions']) == 0:
      flash("Recipe instructions is required.", "instructions")
      is_valid = False
    # check that there's at least 3 characters
    elif len(recipe_data['instructions']) < 3:
      flash("Recipe instructions must have at least 3 characters.", "instructions")
      is_valid = False

    # created at
    # make sure it is not an empty string
    if len(recipe_data['created_at']) == 0:
      flash("Please specify recipe creation date.", "created_at")
      is_valid = False
    
    # under 30 mins
    # make sure it is not an empty string
    if "under_30_mins" not in recipe_data.keys():
    # if len(recipe_data['under_30_mins']) == 0:
      flash("Please specify if recipe takes less than 30 minutes to prepare.", "under_30_mins")
      is_valid = False


    return is_valid