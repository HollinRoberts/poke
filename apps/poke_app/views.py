# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import User,UserManager,Poke
from django.shortcuts import render,redirect,HttpResponse

def index(request):
    print "in index"
    if User.objects.login_check(request):
        user_id=request.session['id']
        active_user=User.objects.get(id=user_id)
        users = User.objects.all().exclude(id=active_user.id)
        poked_by=active_user.recieved.all()
        
        context={'user':active_user,"all":users,"poked":poked_by}
        return render(request,'poke_app/index.html',context)
    else:
        return redirect('/')
def poke_add(request,number):
    print number
    uid=request.session['id']
    initiator=User.objects.get(id=uid)
    print initiator.name
    reciever=User.objects.get(id=number)
    print reciever.name
    
    print reciever.id
    # print initiator.poked.get(id=reciever.id)
    try:
        print "in try"
        count=initiator.poked.get(id=reciever.id).total
        print count
        print "before add"
        count+=1
        print count
        print "after add"
        initiator.poked.get(id=reciever.id).count=count
        initiator.save()
        print initiator.poked.get(id=reciever.id).count
        print "added"
    except:
        poke = Poke.objects.create(total=1,initiator=initiator,reciever=reciever)
        print poke.initiator.name
        print poke.reciever.name
    return redirect("/poke")