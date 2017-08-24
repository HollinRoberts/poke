# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import User,UserManager
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse

def index(request):
    print "in index"
    return render(request,'login_app/index.html')
def login(request):
    if User.objects.login(request.POST,request):
        print 'in if in login'
        return redirect('/poke')
    else:
        print 'login redirect'
        return redirect('/')
def register(request):
    errors = User.objects.basic_validator(request.POST)
    print errors
    if len(errors):
        for tag, error in errors.iteritems():
            print "errors"
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        print 'in submit else'
        User.objects.user_creation(request.POST,request)
        return redirect('/poke')
def logout(request):
    request.session.flush()
    return redirect("/")
