from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

import sys, os 
import json
import requests




from django.shortcuts import render
from django.http import HttpResponse
from . import models

from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse



def register_fun(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        phone = request.POST.get('phone', False)
        email = request.POST.get('email', False)
        print ('im inisde here**************')
        models.register_model(username, password, phone, email)
        return redirect('login')
    return render(request, 'register.html')






def login_fun(request):
    if request.method == 'POST':
        uname = request.POST.get('name', False)
        pwd = request.POST.get('password', False)
        utype = models.login_model(uname, pwd)


        if utype != None:
            request.session['username'] = uname
            request.session['usertype']= utype
            models.is_active(uname, utype)
            if utype == "fans":
                return redirect('homepage')
            else:
                return redirect('celibrityhome')
    else:
        return render(request, 'login.html', {})


    return render(request, 'login.html', {})


def logout_fun(request):
    uname= request.session['username']
    utype= request.session['usertype']
    models.is_inactive(uname,utype)
    request.session.flush()
    return redirect('login')



def online(request):
    online_users=models.is_online(request.session['username']) 
    print(online_users)   
    return render(request,'online.html',{'online_users':online_users})


def chat(request):
    if request.method == 'GET':
        request.session['msg_to'] = request.GET.get('i', '')
        msg_to = request.session['msg_to']
        return render(request, 'chat2.html', {'nameaa':msg_to})
    else:
        msg_to = request.session['msg_to']
        text_msg = request.POST.get('msgbox',False)
        # print text_msg
        msg_from= request.session['username']
        # print "asdfsadag"
        models.chat_db(msg_from,msg_to,text_msg)
        return JsonResponse({'msg':text_msg, 'username': msg_from})




def messages(request):
    msg_from = request.session['username']
    msg_to = request.session['msg_to']

    c = models.get_all_msg_db(msg_from,msg_to)
    print (c)
    return render(request, 'messages.html', {'chat': c})



def homepage(request):
    if request.session.__contains__('username'):
        return render(request, 'Homepage.html',{'userName': request.session['username']})
    else:
        return render(request, 'Homepage.html',{'userName': None})


def Celibritydetail(request):
    if request.session.__contains__('username'):
        return render(request, 'Celibritydetail.html',{'userName': request.session['username']})
    else:
        return render(request, 'Celibritydetail.html',{'userName': None})
    

def celibrityhome(request):
    if request.session.__contains__('username'):
        return render(request, 'Celibrityhome.html',{'userName': request.session['username']})
    else:
        return render(request, 'Celibrityhome.html',{'userName': None})
