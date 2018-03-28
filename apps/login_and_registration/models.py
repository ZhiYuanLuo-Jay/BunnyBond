# -*- coding: utf-8 -*-
# Inside models.py
from __future__ import unicode_literals
from django.db import models
import sys, random, bcrypt
import re, os, binascii 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        # print postData     
        errors = {}
        if len(postData['email']) == 0:
            errors["email"] = "Email needs to be entered."        
        if len(postData['pswd']) == 0:
            errors["pswd"] = "Password needs to be entered."  
        if len(postData['email']) != 0:
            if not EMAIL_REGEX.match(postData['email']):
                errors["format"] = "Email format is not invalid!"
            try:
                user = User.objects.get(email=postData['email'])
                loginEmail = postData['email']
                loginPswd  = postData['pswd']
                user = User.objects.get(email=loginEmail)
                if not bcrypt.checkpw(loginPswd.encode(), user.password.encode()):
                    errors["incorrect"] = "Password Incorrect."
            except:
                errors["email_is_exist"] = "Email address does not exist."
        return errors

    def signup_validator(self, postData):
        # print postData     
        errors = {}
        if len(postData['fn']) < 3:
            errors["fn"] = "Name should be more than 2 characters"
        if len(postData['al']) < 3:
            errors["al"] = "Alias should be more than 2 characters"            
        if len(postData['pasw']) < 8:
            errors["pasw"] = "Password should be more than 7 characters"
        if len(postData['paswcf']) < 8:
            errors["paswcf"] = "Password Confirm should be more than 7 characters"
        if postData['pasw'] != postData['paswcf']:
            errors["match"] = "Password entered not matched."        
        if len(postData['email-regi']) == 0:
            errors["email-regi"] = "Email needs to be entered."
        if not EMAIL_REGEX.match(postData['email-regi']):
            errors["format"] = "Email format is not invalid!"            
        if len(postData['email-regi']) != 0:
            if len(User.objects.filter(email=postData['email-regi'])) != 0:
                errors["email-duplicate"] = "Email exists already."
        return errors


    def add_validator(self, postData):
        # print postData     
        errors = {}
        if len(postData['quoted_by']) < 4:
            errors["quoted_by"] = "Quote by should be more than 3 characters."
        if len(postData['message']) < 11:
            errors["message"] = "Message should be more than 10 characters."            
        return errors        
        

class User(models.Model):
    name       = models.CharField(max_length=255)
    alias      = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)
    password   = models.CharField(max_length=255)
    salt       = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.password, self.salt)
    

class Quote(models.Model):
    quote_name = models.CharField(max_length=255)
    quote_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)    
    user = models.ForeignKey(User, related_name = "added_quotes")
    user_favorites = models.ManyToManyField(User, related_name = "added_favorites")
    def __repr__(self):
        return "<Quote object: {}>".format(self.quote_name)
