# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login as log
from django.contrib.auth import logout as loggedout
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
# Create your views here.
@csrf_exempt
def signup(request):
	if request.method=='POST':
		data = request.body
		data = json.loads(data)
		username = data["username"]
		email = data["email"]
		password = data["password"]
		confirm_password = data["confirm_password"]
		first_name = data["first_name"]
		last_name = data["last_name"]
		type_of_user = data["type_of_user"]

		if password!=confirm_password:
			return JsonResponse({"success":False,"reason":"passwords don't match"})
		user = User(username=username,email=email,first_name=first_name,last_name=last_name)
		user.set_password(password)
		user.is_active=True
		try:
			user.save()
		except:
			return JsonResponse({"success":False,"reason":"user already exists"})

		user_a=authenticate(username=username,password=password)
		if user_a is not None:
			if user_a.is_active:
				log(request,user_a)
		else:
			return HttpResponse({"success":False,"reason":"internal db error"});

		try:		
			UserProfile(user=user,type_of_user=int(type_of_user)).save()
		except:
			return JsonResponse({"success":False,"reason":"internal error"})
		return JsonResponse({"success":True})
	
@csrf_exempt
def addProduct(request):
	if request.method=='POST':
		# import pdb; pdb.set_trace()
		data = request.body
		data = json.loads(data)
		product_name = data["product_name"]
		price = data["price"]
		quantity = data["quantity"]
		# seller_name = data["seller_name"]
		user=None
		try:
			user = User.objects.get(username=request.user.username).profile_info
		except:
			return JsonResponse({"success":False,"reason":"sesssion expired. Please login again."})

		seller_name = request.user.username
		try:
			product = Products(seller=user,product_name=product_name,price=price,quantity=quantity,seller_name=seller_name)
			product.save()
		except:
			return JsonResponse({"success":False,"reason":"Product with this name already exists"})
		return JsonResponse({"success":True})


def logout(request):
    loggedout(request)
    return JsonResponse({"success":True})
@csrf_exempt
def login(request):
    if request.method=="POST":
        data = request.body
        data = json.loads(data)
        username=data["username"]
        password=data["password"]
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                log(request,user) #logging in the user.
                return JsonResponse({"login":True})
        else:
            return JsonResponse({"login":False,"reason":"invalid credentials"})  
