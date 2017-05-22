# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AccessToken(models.Model):
	token_value = models.CharField(max_length=100,unique=True)

class UserProfile(models.Model):
	TYPE = (
		(0,'Admin'),
		(1,'Seller'),
		(2,'Customer'),
	)
	user = models.OneToOneField(User,related_name="profile_info")
	type_of_user=models.IntegerField(choices=TYPE,default=2)
	access_token = models.OneToOneField(AccessToken,related_name="profile_info")
	def __unicode__(self):
		return str(self.user.username)
	
class Tag(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return str(self.name)

class Product(models.Model):
	seller = models.ForeignKey(UserProfile,related_name="product")
	category = models.ManyToManyField(Tag,related_name='products',null=True,blank=True)

	product_name = models.CharField(max_length=200)
	price = models.IntegerField()
	seller_name = models.CharField(max_length=200)
	quantity = models.IntegerField(default=1)
	class Meta:
		unique_together = ('product_name', 'seller_name',)
	def __unicode__(self):
		return str(self.product_name+" by "+self.seller_name)