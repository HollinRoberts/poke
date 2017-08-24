# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from datetime import date,datetime

NAME = re.compile(r'^\w+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD = re.compile(r'[A-Za-z]{8,}')

from django.db import models
class UserManager(models.Manager):
    def email_check(self,postData):
  
        try:
            email=postData['email']
            user=User.objects.filter(email=email)
            user[0].email==email
            return True
        except:
            return False

    def basic_validator(self, postData):
        errors = {}
        if User.objects.email_check(postData):
            errors["user"]="User already exists"
        if len(postData['name'])<2:
            errors['name']="Please enter a name."
        elif not NAME.match(postData['name']):
            errors['name']="Name can only have letters."
        if len(postData['alias'])<2:
            errors['alias']="Please enter an alias."
        if len(postData['email'])==0:
            errors['email']="Please enter an email."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email2']="Improper Email"
        if postData['password']!=postData['confirm']:
            errors['password']="Passwords don't match"
        if not PASSWORD.match(postData['password']):
            errors['password']="Password must have an upercase and lowercase leter."
        try:
            date = postData['birthdate']
            d = datetime.strptime(date, '%Y-%m-%d')
            if d>=datetime.now():
                print "in try if"
                errors['age']="Invalid date"
        except:
            errors['birthdate']="Invalide Birthdate"
        return errors;
        
    def login(self,postData,request):
        email=postData['email']
        user=User.objects.filter(email=email)
        password=postData['password']
        user_password=user[0].password
        if User.objects.email_check(postData) and bcrypt.checkpw(password.encode(),user_password.encode()):
            request.session['id']=user[0].id
            print request.session['id']
            request.session['name']=user[0].name
            print request.session['name']
            return True
        else:
            errors['login']="Login Failed Try Again."
            return False    

    def login_check(self,request):
        try:
            temp = request.session['id']
            print request.session['id']
        except:
            print "no id"
            return False
        return True

    def user_creation(self,postData,request):
        name=postData['name']
        alias=postData['alias']
        email=postData['email']
        password=postData['password']
        password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        birthdate=postData['birthdate']
        created=User.objects.create(name=name,alias=alias,email=email,password=password,birthdate=birthdate)
        request.session['id']=created.id
        print request.session['id']
        request.session['name']=created.name
        print request.session['name']
        return self;

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.name, self.alias, self.email)
    objects = UserManager()

class Poke(models.Model):
    total = models.IntegerField(null=True)
    initiator = models.ForeignKey(User, related_name = "poked",null=True)
    reciever = models.ForeignKey(User, related_name = "recieved",null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    objects = UserManager()