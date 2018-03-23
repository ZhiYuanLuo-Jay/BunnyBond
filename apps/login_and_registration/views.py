# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from django.db import models
from datetime import datetime
from time import gmtime, strftime, localtime
from models import *
from django.contrib import messages
import sys, random, bcrypt


def index(request):  
    return render(request, 'login_and_registration/index.html')  

def login(request):
    if request.method == "POST":
        errors = users.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/login_and_registration") 
        else:
            loginEmail = request.POST['email']
            user = users.objects.get(email=loginEmail)
            # add user session here for different pages
            return render(request, 'login_and_registration/success.html', {'userinfo' : user})  

def register(request):
    if request.method == "POST":
        errors = users.objects.signup_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/login_and_registration") 
        else:
            hash1 = bcrypt.hashpw(request.POST['pasw'].encode(), bcrypt.gensalt())
            users.objects.create(first_name=request.POST['fn'], last_name=request.POST['ln'], \
            email=request.POST['email-regi'], password=hash1, salt=bcrypt.gensalt())
            
            return redirect('/login_and_registration')      
            # user = users.objects.get(id=1)
            # user.password = hash1
            # user.salt = bcrypt.gensalt()
            # user.save()
    