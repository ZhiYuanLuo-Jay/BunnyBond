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
    return render(request, 'bunny_bond/index.html')  


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
            return redirect('/main')


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
            return redirect('/main')      
    
# Dashboard
def home(request):
    userObj = User.objects.get(id=request.session['user_id'])
    dataset1 = Bill.objects.filter(user=userObj)

    # Bill item list
    billList = []
    for i in dataset1: 
        # print i # bill object
        billList += [{
            'bill_id'      : i.id,
            'bill_name'    : i.bill_name,
            'bill_amount'  : i.bill_amount,
            'bill_user_name': User.objects.get(id=i.user_id).name,
            'bill_due_date': i.due_date.strftime("%b %d, %Y"),
            'bill_user_id' : i.user_id
            }]   
    # print billList

    billSum = 0
    for amt in billList:
        # print amt['bill_amount']    
        billSum += amt['bill_amount']    
    request.session['bill_balance'] = float(billSum)
    # print request.session['bill_balance']

    dataset2 = Task.objects.exclude(task_completed__contains=1)
    taskList = []
    for i in dataset2: 
        # print i # task object
        taskList += [{
            'task_id'         : i.id,
            'task_name'       : i.task_name,
            'star_amount'     : i.star_amount,
            'task_work_date'  : i.work_date.strftime("%b %d, %Y"),
            'task_creator_id' : i.creator_id,
            'task_posted_by'  : User.objects.get(id=i.creator_id).name
            }]   
    # print taskList

    dataset3 = Task.objects.filter(task_completed__contains=1) & Task.objects.filter(finisher=userObj)
    sAmountSum = 0
    for i in dataset3:
        # print i.star_amount
        sAmountSum += i.star_amount
    request.session['star_earned'] = sAmountSum

    dataset4 = Funding.objects.all()
    fundSum = 0
    for i in dataset4:
        # print dataset4
        fundSum += float(i.donation_amount)
    request.session['fund_amount'] = fundSum

    context = {
        'all_bills' : billList,
        'all_tasks' : taskList
    }
    return render(request, 'bunny_bond/home.html', context)  


def seebill(request):
    return render(request, 'bunny_bond/create_b.html')  

def seetask(request):
    return render(request, 'bunny_bond/create_t.html')  

def seefund(request):
    return render(request, 'bunny_bond/donation.html')  
    

def addingBill(request):
    if request.method == "POST":
        errors = User.objects.add_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/cBill") 
        else:  
            userObj = User.objects.get(id=request.session['user_id'])
            Bill.objects.create(bill_name=request.POST['bill_name'], bill_amount=request.POST['bill_amount'], \
            due_date=request.POST['due_date'], user=userObj)
            return redirect("/main") 

def addingTask(request):
    if request.method == "POST":
        errors = User.objects.task_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/cTask") 
        else:  
            userObj = User.objects.get(id=request.session['user_id'])
            Task.objects.create(task_name=request.POST['task_name'], star_amount=request.POST['star_amount'], \
            work_date=request.POST['work_date'], task_completed=False, creator=userObj)
            return redirect("/main")

def addingFund(request):
    # if request.method == "POST":
    #     errors = User.objects.task_validator(request.POST)
    #     if len(errors):
    #         for tag, error in errors.iteritems():
    #             messages.error(request, error, extra_tags=tag)
    #         return redirect("/cTask") 
    #     else:  
    userObj = User.objects.get(id=request.session['user_id'])
    Funding.objects.create(donation_amount=request.POST['donation_amount'], message=request.POST['message'], \
    donator=userObj)
    return redirect("/main")

def acceptTask(request, id):
    print id
    userObj = User.objects.get(id=request.session['user_id'])
    taskObj = Task.objects.get(id=id)
    userObj.jobs.add(taskObj)
    tCur = taskObj
    tCur.task_completed = 1
    tCur.save()

    # Funding.objects.create(donation_amount=request.POST['donation_amount'], message=request.POST['message'], \
    # donator=userObj)
    return redirect("/main")

def paidRemove(request, id):
    Bill.objects.filter(id=id, user_id=request.session['user_id'] ).delete()
    return redirect("/main") 

def disp(request, id):
    userObj = User.objects.get(id=id)  # create userObj
    request.session['task_creator'] = userObj.name
    numInfo = len(userObj.tasks.all())
    request.session['num_info'] = numInfo
    # print numInfo

    uInfo1 = userObj.tasks.all()

    uInfo = []
    for i in uInfo1: 
        # print i # task object
        uInfo += [{
            'task_id'         : i.id,
            'task_name'       : i.task_name,
            'star_amount'     : i.star_amount,
            # 'task_work_date'  : i.work_date.strftime("%b %d, %Y"),
            'post_creator_id' : i.creator_id,
            'post_by'         : User.objects.get(id=i.creator_id).name
            }] 
    return render(request, 'bunny_bond/info.html', {'user_infos' : uInfo})  



# def addingFav(request, id):
#     print id
#     userObj = User.objects.get(id=request.session['user_id'])  # create userObj
#     quoteObj = Quote.objects.get(id=id)
#     userObj.added_favorites.add(quoteObj)   # userObj add a favorite to list
#     return redirect("/main")     


# def remove(request, id):
#     userObj = User.objects.get(id=request.session['user_id'])
#     quoteObj = Quote.objects.get(id=id)
#     userObj.added_favorites.remove(quoteObj)
#     return redirect("/main") 




def logoff(request):
    # request.session['user_id'] = ""
    request.session.flush()
    return render(request, 'bunny_bond/index.html')  














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


