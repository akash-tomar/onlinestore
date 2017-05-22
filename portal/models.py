# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
	TYPE = (
		(0,'Admin'),
		(1,'Seller'),
		(2,'Customer'),
	)
	user = models.OneToOneField(User,related_name="profile_info")
	type_of_user=models.IntegerField(choices=TYPE,default=2)
	
class Tag(models.Model):
	name = models.CharField(max_length=200)

class Product(models.Model):
	seller = models.ForeignKey(UserProfile,related_name="product")
	category = models.ManyToManyField(Tag,related_name='products',null=True,blank=True)

	product_name = models.CharField(max_length=200,unique=True)
	price = models.IntegerField()
	seller_name = models.CharField(max_length=200)
	quantity = models.IntegerField(default=1)
