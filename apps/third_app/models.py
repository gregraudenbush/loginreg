from __future__ import unicode_literals
from django.db import models
from datetime import datetime 
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def login(self, post):
        errors = []
       
        user_list = User.objects.filter(email = post['email'])
        if user_list:
            db_hashed = user_list[0].password
            if db_hashed == bcrypt.hashpw(post['password'].encode(), db_hashed.encode()):
                return {"status": True, "data": user_list[0]}
            else: 
                errors.append("Incorrect Password")
        else:
            errors.append("Email not found")
        return {"status": False, "data": errors}
        

    def val(self, post):
        # first_name, last_name, email, password, password2

        errors = []
        user = post['first_name']
        
        if len(post['email']) < 1 or len(post['first_name']) < 1 or len(post['last_name']) < 1 or len(post['alias']) < 1:
            errors.append("Please Complete The Form")
        
        if not EMAIL_REGEX.match(post['email']):
            errors.append("Email must include @ ")

        if len(post['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        elif post['password'] != post['password2']:
            errors.append("Passwords do not match")

        if not errors:
            if User.objects.filter(email = post['email']).exists():
                errors.append("Email alredy exists in database")
            else:
                hashed_pw = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())  
                user = User.objects.create(first_name = post['first_name'], last_name = post['last_name'], alias = post['alias'], email=post['email'],password=hashed_pw, dob = post['dob'])
                return {"status": True, "data": user}


        return {"status": False, "data": errors}
            
class User(models.Model):
    first_name = models.CharField(max_length=38, default = "")
    last_name = models.CharField(max_length=38, default = "")
    alias = models.CharField(max_length=38, default = "")
    email = models.CharField(max_length=38, default = "")
    password = models.CharField(max_length=38, default = "")
    dob = models.DateTimeField()
    added = models.DateTimeField(auto_now = True)
    objects = UserManager()

# class PokeManager(models.Manager):
#     def poking(self, post):
#         poke = Poke.objects.create(user = User.objects.get(id = post['user']), userpoked = User.objects.get(id = post['userpoked']))
#         return {"status": True, "data": poke}
class Poke(models.Model):
   
    user = models.ForeignKey(User, related_name="poker")
    userpoked = models.ForeignKey(User, related_name="poked")
    
    added = models.DateTimeField(auto_now = True)
    # objects = PokeManager()