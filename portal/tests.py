# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import json
# Create your tests here.
# access_token=""
class SignUpTest(TestCase):
	def Test_createAccount(self):
		my_data = {'username': 'akash.tomar107', 'password': 'akashtomar',"email":"akash.tomar217@gmail.com", "confirm_password":"akashtomar", "type_of_user":"1", "first_name":"akash", "last_name":"tomar"}
		response = self.client.post('/signup/', json.dumps(my_data), content_type='application/json')
		self.access_token = json.loads(response.content)["access_token"]
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_login(self):
		my_data = {'username': 'akash.tomar107', 'password': 'akashtomar'}
		response = self.client.post('/login/', json.dumps(my_data), content_type='application/json')
		self.assertIs(json.loads(response.content)["login"], True)

	def Test_add_product(self):
		my_data = {"product_name":"prod 2","price":"120","quantity":"4","category": ["akash","akash tomar"]}
		import pdb; pdb.set_trace()
		response = self.client.post('/addproduct/', json.dumps(my_data), content_type='application/json', Authorization=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def Test_search(self):
		my_data = {"product_name":"prod 2","price":"120","quantity":"4","category": ["akash","akash tomar"]}
		import pdb; pdb.set_trace()
		response = self.client.post('/addproduct/', json.dumps(my_data), content_type='application/json', Authorization=self.access_token)
		self.assertIs(json.loads(response.content)["success"], True)

	def test_run(self):
		self.Test_createAccount()
		self.Test_login()
		self.Test_add_product()