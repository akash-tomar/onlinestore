# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import json
from random import randint
# Create your tests here.
# access_token=""
class SignUpTest(TestCase):
	def Test_createAccount(self,my_data):
		response = self.client.post('/signup/', json.dumps(my_data), content_type='application/json')
		self.access_token = json.loads(response.content)["access_token"]
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_login(self,my_data):
		response = self.client.post('/login/', json.dumps(my_data), content_type='application/json')
		self.assertIs(json.loads(response.content)["login"], True)

	def Test_add_product(self,my_data):
		response = self.client.post('/addproduct/', json.dumps(my_data), content_type='application/json', HTTP_AUTHORIZATION=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_search(self,query):
		response = self.client.get('/search/?q='+query,content_type='application/json', HTTP_AUTHORIZATION=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_update(self,my_data):
		response = self.client.post('/update/',json.dumps(my_data), content_type='application/json', HTTP_AUTHORIZATION=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_getproduct(self,seller_name,product_name):
		response = self.client.get('/getproduct/?seller_name='+seller_name+'&product_name='+product_name,content_type='application/json', HTTP_AUTHORIZATION=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_delete(self,my_data): 
		response = self.client.delete('/deleteproduct/',json.dumps(my_data), content_type='application/json', HTTP_AUTHORIZATION=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)


	def test_A(self):
		usernames=[]
		emails = []
		first_names=[]
		last_names=[]
		passwords=[]
		with open('testcases/username.txt') as file:
			file = file.readlines()
			for f in file:
				usernames.append(f[:len(f)-1])

		with open('testcases/email.txt') as file:
			file = file.readlines()
			for f in file:
				emails.append(f[:len(f)-1])

		with open('testcases/password.txt') as file:
			file = file.readlines()
			for f in file:
				passwords.append(f[:len(f)-1])

		with open('testcases/names.txt') as file:
			file = file.readlines()
			for f in file:
				f = unicode(f, 'utf-8')
				temp = f.split(' ')
				first_names.append(temp[0])
				last_names.append(temp[1])


		for i in range(50):
			signup_details = {'username': usernames[i], 'password': passwords[i],"email":emails[i], "confirm_password":passwords[i], "type_of_user":"2", "first_name":first_names[i], "last_name":last_names[i]}
			self.Test_createAccount(signup_details)


		for i in range(50):
			login_detials = {'username': usernames[i], 'password': passwords[i]}
			self.Test_login(login_detials)

		
		products=[]
		with open('testcases/product.txt') as file:
			file = file.readlines()
			for f in file:
				products.append(f[:len(f)-1])

		tags=[]
		with open('testcases/tags.txt') as file:
			file = file.readlines()
			for f in file:
				tags.append(f[:len(f)-1])

		for i in products:
			index = randint(1,10)
			category=[]
			for j in range(index):
				z = randint(0,49)
				category.append(tags[z])
			add_product = {"product_name":i,"price":randint(100,100000),"quantity":randint(1,100),"category": category}
			self.Test_add_product(add_product)
		
		for i in tags:
			self.Test_search(i)

		for i in products:
			update = {"product_name":i,"price":"120","quantity":"4866875875","category": ["akash","tomar"]}
			self.Test_getproduct("snarldover",i)
			self.Test_update(update)
			delete = {"product_name":i}
			self.Test_delete(delete)