from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re
# model the class after the book table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "log_and_reg_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # list of the authors who have favorited this book
        self.users = []


    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of emails
        users = []
        # Iterate over the db results and create instances of books with cls.
        for u in results:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from users WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data) 
        return results


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('log_and_reg_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
        
        


    @staticmethod
    def validate(user):
        isValid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL('log_and_reg_scheme').query_db(query)
        if len() >= 1:
            isValid = False
            flash("That email is already in the system!")

        if len(user['first_name']) < 2:
            isValid = False 
            flash("First name must be at least 2 characters long")

        if len(user['last_name']) < 2:
            isValid = False 
            flash("Last name must be at least 2 characters long")

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!" , "email")
        
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters long")
            isValid=False 

        if user['password'] != user['confirm_password']:
            isValid = False
            flash("Your Passwords don't match")
        return isValid

    
    