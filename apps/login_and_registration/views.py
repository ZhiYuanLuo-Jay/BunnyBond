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
            # pull user info from database
            loginEmail = request.POST['email']
            user = User.objects.get(email=loginEmail)
            request.session['user_id'] = user.id            
            request.session['user_name'] = user.name       # used in html    
            return redirect('/quotes')


def register(request):
    if request.method == "POST":
        errors = User.objects.signup_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/") 
        else:
            # save email
            hash1 = bcrypt.hashpw(request.POST['pasw'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['fn'], alias=request.POST['al'], \
            email=request.POST['email-regi'], password=hash1, salt=bcrypt.gensalt())
            
            # pull user info from database
            loginEmail = request.POST['email-regi']
            user = User.objects.get(email=loginEmail)
            request.session['user_id'] = user.id            
            request.session['user_name'] = user.name     # used in html
            return redirect('/quotes')      
    
# Dashboard
def home(request):
    userObj = User.objects.get(id=request.session['user_id'])
    dataset1 = Quote.objects.exclude(user_favorites=userObj)

    # user item list
    quoteList = []
    for i in dataset1: 
        # print i # item object
        quoteList += [{
            'quote_id' :   i.id,
            'quote_name' : i.quote_name,
            'quote_message' : i.quote_message,
            'posted_by' :  User.objects.get(id=i.user_id).name,
            'user_id'  :  i.user_id
            }]   
    # print quoteList

    dataset2 = userObj.added_favorites.all()
    favList = []
    for i in dataset2: 
        # print i # item object
        favList += [{
            'fav_id' :   i.id,
            'fav_name' : i.quote_name,
            'fav_message' : i.quote_message,
            'fav_posted_by' :  User.objects.get(id=i.user_id).name,
            'fav_user_id'  :  i.user_id
            }]   
    # print favList

    context = {
        'all_quotes' : quoteList,
        'all_favor' : favList
    }
    return render(request, 'login_and_registration/quotes.html', context)  


def adding(request):
    if request.method == "POST":
        errors = User.objects.add_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/quotes") 
        else:  
            userObj = User.objects.get(id=request.session['user_id'])
            # print request.POST['quoted_by']
            # print request.POST['message']
            Quote.objects.create(quote_name=request.POST['quoted_by'], quote_message=request.POST['message'], user=userObj)
            return redirect("/quotes") 

def addingFav(request, id):
    print id
    userObj = User.objects.get(id=request.session['user_id'])  # create userObj
    quoteObj = Quote.objects.get(id=id)
    userObj.added_favorites.add(quoteObj)   # userObj add a favorite to list
    return redirect("/quotes")     


def remove(request, id):
    userObj = User.objects.get(id=request.session['user_id'])
    quoteObj = Quote.objects.get(id=id)
    userObj.added_favorites.remove(quoteObj)
    return redirect("/quotes") 


def disp(request, id):
    userObj = User.objects.get(id=id)  # create userObj
    request.session['post_by_name'] = userObj.name
    numInfo = len(userObj.added_quotes.all())
    request.session['num_info'] = numInfo

    info1 = userObj.added_quotes.all()
    infoList = []
    for i in info1: 
        # print i # item object
        infoList += [{
            'quote_id' :   i.id,
            'quote_name' : i.quote_name,
            'quote_message' : i.quote_message,
            'posted_by' :  User.objects.get(id=i.user_id).name,
            'user_id'  :  i.user_id
            }] 

    return render(request, 'login_and_registration/info.html', {'quote_info' : infoList})  


def logoff(request):
    # request.session['user_id'] = ""
    request.session.flush()
    return render(request, 'login_and_registration/index.html')  


    # # set 1, items item
    # userObj= User.objects.get(id=request.session['user_id'])        
    # # dataset1 = userObj.added_wishes.all()               # return all items, userObj interested and created       -- many to many  reverse look-up
    # dataset1 = Item.objects.filter(user_wishes=userObj)   # return all items, only userObj interested and created  -- many to many
        
    # # user item list
    # itemList = []
    # for i in dataset1: 
    #     # print i # item object
    #     itemList += [{
    #         'item_id' :   i.id,
    #         'item_name' : i.item_name,
    #         'added_by' :  User.objects.get(id=i.user_id).first_name,
    #         'date_added': i.created_at.strftime("%b %d, %Y"),
    #         'user_id'  :  i.user_id
    #         }]   
    # # print itemList

    # # other item list 
    # # dataset2 = Item.objects.exclude(user=userObj) # return all items, not created by userObj. -- one to many
    # # dataset2 = Item.objects.filter(user=userObj)  # return all items, created by userObj.     -- one to many
    # # dataset2 = Item.objects.filter(user_wishes=userObj) # return all itmes, only userObj interested and created.         -- many to many
    # dataset2 = Item.objects.exclude(user_wishes=userObj) # return all items, not userObj interested and userObjc created.  -- many to many
    
    # otherList = []
    # for i in dataset2: 
    #     otherList += [{
    #         'item_id' :   i.id,
    #         'item_name' : i.item_name,
    #         'added_by' :  User.objects.get(id=i.user_id).first_name,
    #         'date_added' : i.created_at.strftime("%b %d, %Y"),
    #         'user_id':     i.user_id
    #         }]       
    
    # context = {
    #     'item_all' : itemList,
    #     'other_list' : otherList
    # }
    
    # return render(request, 'login_and_registration/items.html', context)  


# def additem(request):
#     return render(request, 'login_and_registration/create.html')  



# def addingWL(request, id):
#     # print id
#     userObj = User.objects.get(id=request.session['user_id'])  # create userObj
#     itemObj = Item.objects.get(id=id)   # create itemObj
#     userObj.added_wishes.add(itemObj)   # userObj add a wish to list
#     return redirect("/dashboard") 


# def disp(request, id):
#     itemObj = Item.objects.get(id=id)  # create itemObj
#     wish_user = itemObj.user_wishes.all()  # return all users for the specific item id
#     return render(request, 'login_and_registration/iteminfo.html', {'all_wish_user' : wish_user})  


# def delete(request, id):
#     Item.objects.filter(id=id, user_id=request.session['user_id'] ).delete()
#     return redirect("/dashboard") 


