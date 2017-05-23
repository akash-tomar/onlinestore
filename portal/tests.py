# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import json
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
		signup_details = {'username': 'akashtomar107', 'password': 'akashtomar',"email":"akash.tomar217@gmail.com", "confirm_password":"akashtomar", "type_of_user":"1", "first_name":"akash", "last_name":"tomar"}
		self.Test_createAccount(signup_details)

		login_detials = {'username': 'akashtomar107', 'password': 'akashtomar'}
		self.Test_login(login_detials)

		add_product = {"product_name":"prod2","price":"120","quantity":"4","category": ["akash","akash tomar"]}
		self.Test_add_product(add_product)
		
		self.Test_search("akash")

		update = {"product_name":"prod2","price":"120","quantity":"4866875875","category": ["akash","tomar"]}
		self.Test_update(update)
		self.Test_getproduct("akashtomar107","prod2")
		delete = {"product_name":"prod2"}
		self.Test_delete(delete)