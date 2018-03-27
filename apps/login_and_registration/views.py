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
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/") 
        else:
            loginEmail = request.POST['email']
            user = User.objects.get(email=loginEmail)
            request.session['user_id'] = user.id            
            request.session['user_name'] = user.first_name                
            return redirect('/dashboard')


def register(request):
    if request.method == "POST":
        errors = User.objects.signup_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/") 
        else:
            hash1 = bcrypt.hashpw(request.POST['pasw'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['fn'], last_name=request.POST['ln'], \
            email=request.POST['email-regi'], password=hash1, salt=bcrypt.gensalt())
            # save email, pull user info from database
            loginEmail = request.POST['email-regi']
            user = User.objects.get(email=loginEmail)
            request.session['user_id'] = user.id            
            request.session['user_name'] = user.first_name              
            return redirect('/dashboard')      
    
# Dashboard
def tohome(request):
    # set 1, items item
    userObj= User.objects.get(id=request.session['user_id'])        
    dataset1 = userObj.added_wishes.all() 

    # user item list
    itemList = []
    for i in dataset1: 
        itemList += [{
            'item_id' :   i.id,
            'item_name' : i.item_name,
            'added_by' :  User.objects.get(id=i.user_id).first_name,
            'date_added' : i.created_at.strftime("%b %d, %Y"),
            'user_id':     i.user_id
            }]   

    # other item list 
    userCur = User.objects.get(id=request.session['user_id'])
    # dataset2 = Item.objects.exclude(user_wishes=request.session['user_id'])   # works the same below
    dataset2 = Item.objects.exclude(user_wishes=userCur)
    otherList = []
    for i in dataset2: 
        otherList += [{
            'item_id' :   i.id,
            'item_name' : i.item_name,
            'added_by' :  User.objects.get(id=i.user_id).first_name,
            'date_added' : i.created_at.strftime("%b %d, %Y"),
            'user_id':     i.user_id
            }]       
    
    context = {
        'item_all' : itemList,
        'other_list' : otherList
    }
    
    return render(request, 'login_and_registration/items.html', context)  


def additem(request):
    return render(request, 'login_and_registration/create.html')  


def adding(request):
    if request.method == "POST":
        errors = User.objects.add_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/wish_items/create") 
        else:  
            userObj = User.objects.get(id=request.session['user_id'])
            Item.objects.create(item_name=request.POST['product'], user=userObj)
            userObj.added_wishes.add(Item.objects.last())
            return redirect("/dashboard") 


def addingWL(request, id):
    # print id
    userObj = User.objects.get(id=request.session['user_id'])
    # print userObj.first_name
    wishItemObj = Item.objects.get(id=id)
    # print wishItemObj.item_name
    userObj.added_wishes.add(wishItemObj)
    return redirect("/dashboard") 


def disp(request, id):
    item = Item.objects.get(id=id)
    # print item.item_name
    # print item.id
    wish_user = item.user_wishes.all()
    # for usr in wish_user:
    #     print usr.first_name
    return render(request, 'login_and_registration/iteminfo.html', {'all_wish_user' : wish_user})  


def delete(request, id):
    Item.objects.filter(id = id, user_id = request.session['user_id'] ).delete()
    return redirect("/dashboard") 


def remove(request, id):
    userObj = User.objects.get(id=request.session['user_id'])
    userObj.added_wishes.remove(Item.objects.get(id=id))
    return redirect("/dashboard") 


def logoff(request):
    request.session['user_id'] = ""
    request.session['user_name'] = ""
    return render(request, 'login_and_registration/index.html')  