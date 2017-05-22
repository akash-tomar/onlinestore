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
import re
from django.db.models import Q
import uuid
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

		access_token = str(uuid.uuid4().get_hex())
		try:
			at = AccessToken(token_value=access_token)
			at.save()
			UserProfile(user=user,type_of_user=int(type_of_user),access_token=at).save()
		except:
			return JsonResponse({"success":False,"reason":"internal error"})
		return JsonResponse({"success":True,"access_token":access_token})
	
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
				access_token = user.profile_info.access_token.token_value
				return JsonResponse({"login":True,"access_token":access_token})
		else:
			return JsonResponse({"login":False,"reason":"invalid credentials"})  

def checkToken(request):
	if "HTTP_AUTHORIZATION" in request.META:
		token = request.META["HTTP_AUTHORIZATION"]
		if AccessToken.objects.exists(token_value=token):
			return True
	return False

@csrf_exempt
def addProduct(request):
	if not checkToken(request):
		return JsonResponse({"success":False,"reason":"authentication failed"})

	if request.method=='POST':
		data = request.body
		data = json.loads(data)
		product_name = data["product_name"]
		price = data["price"]
		quantity = data["quantity"]
		category = data["category"]

		list_category=[]
		for i in category:
			Tag.objects.get_or_create(name=i)
			list_category.append(Tag.objects.get(name=i))
		user = AccessToken.objects.get(token_value=token).profile_info
		# try:
		# 	user = User.objects.get(username=request.user.username).profile_info
		# except:
		# 	return JsonResponse({"success":False,"reason":"sesssion expired. Please login again."})

		seller_name = user.user.username
		
		try:
			print list_category
			product = Product(seller=user,product_name=product_name,price=price,quantity=quantity,seller_name=seller_name)
			product.save()
			for i in list_category:
				product.category.add(i)
			product.save()
		except:
			return JsonResponse({"success":False,"reason":"Product with this name already exists"})
		return JsonResponse({"success":True})

@csrf_exempt
def deleteProduct(request):
	if not checkToken(request):
		return JsonResponse({"success":False,"reason":"authentication failed"})

	if request.method=="DELETE":
		data = request.body
		data = json.loads(data)
		product_name = data["product_name"]
		# seller_name = data["seller_name"]

		seller_name = AccessToken.objects.get(token_value=token).profile_info.seller_name

		try:
			prod = Product.objects.get(product_name=product_name,seller_name=seller_name)
			prod.delete()
			return JsonResponse({"success":True})
		except:
			return JsonResponse({"success":False,"reason":"No such product exists with this seller name"})


def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):

	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
	query = None # Query to search for every search term
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query


def search(request):
	if not checkToken(request):
		return JsonResponse({"success":False,"reason":"authentication failed"})

	keyword=request.GET['q']
	tagval = keyword.strip()

	product_query = get_query(keyword.strip(), ['product_name','seller_name',])
	tag_query = get_query(keyword.strip(), ['name',])
	products = Product.objects.filter(product_query).distinct().order_by('id').reverse()

	prod_list = []
	for prod in products:
		prod_list.append(prod.product_name)

	tags = Tag.objects.filter(tag_query).distinct().order_by('id').reverse()
	tag_list={}
	for tag in tags:
		prods = tag.products.all()
		tag_list[tag.name]=[]
		for prod  in prods:
			tag_list[tag.name].append(prod.product_name)
	return JsonResponse({"products":prod_list,"tags":tag_list})

@csrf_exempt
def update(request):
	if not checkToken(request):
		return JsonResponse({"success":False,"reason":"authentication failed"})

	if request.method=='POST':
		data = request.body
		data = json.loads(data)

		product_name = data["product_name"]

		user_profile = AccessToken.objects.get(token_value=token).profile_info
		seller_name = user_profile.seller_name
		# seller_name = request.user.username
		# if "seller_name" in data:
		# 	seller_name = data["seller_name"]

		prod = None
		try:
			prod = Product.objects.get(product_name=product_name,seller_name=seller_name)
		except:
			return JsonResponse({"success":False,"reason":"Invalid couple of product and seller name."})

		if "price" in data:
			prod.price=data["price"]
		if "quantity" in data:
			prod.quantity=data['quantity']
		if 'category' in data:
			prod.category.clear()
			for i in data["category"]:
				Tag.objects.get_or_create(name=i)
				prod.category.add(Tag.objects.get(name=i))
		prod.save()
		return JsonResponse({"success":True})