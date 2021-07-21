# import the function that will return an instance of a connection
from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash
from recipes_app.models import recipe
import re
from recipes_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# import datetime

# create a regular expression object that we'll use later
NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# BIRTHDAY_REGEX = re.compile(r'^\d{4}\-\d{2}\-\d{2}$')
# DATE_REGEX = re.compile(r'^\d{2}\/\d{2}\/\d{4}$')

class User:
  def __init__(self, data):
    self.id = data['id']
    self.first_name = data['first_name']
    self.last_name = data['last_name']
    self.email = data['email']
    self.password = data['password']    
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    # self.recipes = []

  # Classmethods for registration
  # this method returns True if user is in our database, returns False if user does not exist
  @classmethod
  def user_exists(cls, data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    results = connectToMySQL('recipes').query_db(query, data)
    if len(results) != 0:
      return True
    else:
      return False
  
  @classmethod
  def save(cls, data):
    query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
    return connectToMySQL('recipes').query_db(query, data)

  # classmethods for login
  @classmethod
  def get_user_by_email(cls,data):
      query = "SELECT * FROM users WHERE email = %(email)s;"
      result = connectToMySQL("recipes").query_db(query,data)
      # Didn't find a matching user
      if len(result) < 1:
          return False
      return cls(result[0])
  
  @classmethod
  def get_user_by_id(cls, data):
    query = "SELECT * FROM users WHERE id = %(user_id)s;"
    result = connectToMySQL("recipes").query_db(query,data)
    # Didn't find a matching user
    if len(result) < 1:
        return False
    return cls(result[0])
  
  # @classmethod
  # def get_all(cls):
  #   query = "SELECT * FROM emails"
  #   results = connectToMySQL('email').query_db(query)

  #       #create an empty list to store all instances of dojos
  #   emails = []
  #   # iterate over db results and create instances of dojos with cls
  #   for email in results:
  #     emails.append( cls(email) )
  #   return emails



  # # @classmethod
  # # def is_duplicate(cls, email):
  # #   data = {
  # #     "email" : email
  # #   }
  # #   query = "SELECT * FROM emails WHERE email = %(email)s;"
  # #   results = connectToMySQL('email').query_db(query, data)
  # #   if len(results) != 0:
  # #     return True
  # #   else:
  # #     return False
  
  # # @classmethod
  # # def delete(cls,data):
  # #   query = "DELETE FROM emails WHERE id = %(email_id)s;"
  # #   return connectToMySQL('email').query_db(query, data)




  
  # # get messages that user has received, returns instance of user with all messages stored in a list in user.messages
  # @classmethod
  # def get_user_with_messages ( cls, data ):
  #   # query = "SELECT * FROM users LEFT JOIN messages ON users.id = messages.recipient_id WHERE users.id = %(user_id)s;"
  #   # this query will allow me to get all the messages for the current user, including the sender's details.
  #   # for refactoring, consider returning list of dictionary instead of instances of message class
  #   query = "SELECT * FROM users JOIN messages ON users.id = messages.user_id WHERE messages.recipient_id = %(user_id)s;"
  #   results = connectToMySQL('recipes').query_db(query, data)

  #   # create an instance of user class
  #   user = cls( results[0] )
  #   print(results)
  #   for row_from_db in results:
  #     # in case there is a row of data with user but no message
  #     if row_from_db['messages.id'] != None:
  #       message_data = {
  #         "id" : row_from_db['messages.id'],
  #         "message" : row_from_db["message"],
  #         "recipient_id"  : row_from_db["recipient_id"],
  #         "user_id" : row_from_db["user_id"],
  #         "created_at" : row_from_db["messages.created_at"],
  #         "updated_at" : row_from_db["messages.updated_at"]
  #       }
  #       # user.messages.append(message.Message(message_data))
  #   return user

  # @classmethod
  # def get_user_recipients(cls, data):
  #   query = "SELECT * FROM users WHERE users.id != %(user_id)s ORDER BY first_name;"
  #   results = connectToMySQL('recipes').query_db(query, data)
  #   recipients = []
  #   # iterate over db results and create instances of dojos with cls
  #   for user in results:
  #     recipients.append( cls(user) )
  #   return recipients



  @staticmethod
  def validate_registration(user): #takes in request.form input as argument
      is_valid = True # we assume this is true

      # first name
      # make sure it is not an empty string
      if len(user['first_name']) == 0:
        flash("First name is required.", "first_name")
        is_valid = False
      # check that there's at least 2 characters
      elif len(user['first_name']) < 2:
        flash("First name must have at least 2 characters.", "first_name")
        is_valid = False
      # # check that first name only contains letters
      # elif not NAME_REGEX.match(user['first_name']):
      #   flash("First name must not contain non-alphabetic characters.", "first_name")
      #   is_valid = False
      
      # last name
      # make sure it is not an empty string
      if len(user['last_name']) == 0:
        flash("Last name is required.", "last_name")
        is_valid = False
      # check that there's at least 2 characters
      elif len(user['last_name']) < 2:
        flash("Last name must have at least 2 characters.", "last_name")
        is_valid = False
      # # check that first name only contains letters
      # elif not NAME_REGEX.match(user['last_name']):
      #   flash("Last name must not contain non-alphabetic characters.", "last_name")
      #   is_valid = False

      # email
      # check if email is submitted
      if len(user['email']) == 0:
        flash("Email is required", "email")
        is_valid = False
      # invalid email format
      elif not EMAIL_REGEX.match(user['email']): 
        flash("Invalid email address format.", "email")
        is_valid = False
      # check whether user exist
      # elif User.user_exists({"email": user['email']}):
      elif User.user_exists(user):
        flash("Email already registered!", "email")
        is_valid = False
      
      # password
      # check for submission
      if len(user['password']) == 0:
        flash("Password is required", "password")
        is_valid = False
      # must be at least 8 characters
      elif len(user['password']) < 8:
        flash("Password must have at least 8 characters", "password")
        is_valid = False
      # # make sure there's one capital letter and one number
      # elif re.search('[0-9]',user['password']) is None or re.search('[A-Z]',user['password']) is None:
      #   flash("Password must contain a number and a capital letter", "password")
      #   is_valid = False
      # make sure password and confirm password matches
      elif user['confirm_pw'] != user['password']:
        flash("Confirm password does not match password", "password")
        is_valid = False
      return is_valid
  
  @staticmethod
  # here user should contain email and password
  def validate_login(login_user):
    # user is not registered in the db
    user_in_db = User.get_user_by_email(login_user)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return False
    # if user is registered, check if password matches
    if not bcrypt.check_password_hash(user_in_db.password, login_user['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return False
    return user_in_db
  
