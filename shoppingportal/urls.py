"""shoppingportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from portal.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/',signup,name='signup'),
    url(r'^addproduct/',addProduct,name='addproduct'),
    url(r'^logout/',logout,name='logout'),
    url(r'^login/',login,name='login'),
    url(r'^deleteproduct/',deleteProduct,name='deleteproduct'),
	url(r'^search/',search,name='search'),
	url(r'^update/',update,name='update'),
	url(r'^getproduct/',getProduct,name='getproduct'),
]
