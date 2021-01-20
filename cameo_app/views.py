from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

import sys, os 
import json
import requests
import datetime




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
            models.chat_end(uname)
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
        uname = request.session['username']
        count = models.notification_count(uname)
        status = models.chat_start(uname)
        print(status)
        if status == True:
            otheruser  = models.other_user(uname)
            return render(request, 'Homepage.html',{'userName': request.session['username'],'count':count,'status':status,'otheruser':otheruser})
        return render(request, 'Homepage.html',{'userName': request.session['username'],'count':count,'status':False})
    else:
        return render(request, 'Homepage.html',{'userName': None,'status':False})


def Celibritydetail(request):
    if request.method == 'POST':
        celebrityname = request.POST.get('celibrity_name', False)
        lastname, feature, description, videorate, chatrate = models.celebrity_model(celebrityname)
        data = models.comments(celebrityname)
        if request.session.__contains__('username'):
            uname = request.session['username']
            count = models.notification_count(uname)
            status = models.chat_start(uname)
            if status == True:
                otheruser  = models.other_user(uname)
                return render(request, 'Celibritydetail.html',{'userName': request.session['username'],
                'celebrityname':celebrityname,'lastname':lastname,'feature':feature,
                'description':description,'videorate':videorate,'chatrate':chatrate,'count':count,'datas': list(data),'status':status,'otheruser':otheruser})
            return render(request, 'Celibritydetail.html',{'userName': request.session['username'],
            'celebrityname':celebrityname,'lastname':lastname,'feature':feature,
            'description':description,'videorate':videorate,'chatrate':chatrate,'count':count,'datas': list(data),'status':False})
        else:
            userlogin = "nouser"
            return render(request, 'Celibritydetail.html',{'userName': None,
            'celebrityname':celebrityname,'lastname':lastname,'feature':feature,
            'description':description,'videorate':videorate,'chatrate':chatrate,'userlogin':userlogin,'datas': list(data),'status':False})



    

def celibrityhome(request):
    username = request.session['username']
    data = models.celebrity_request_model(username,'video')
    chatdata = models.celebrity_request_model(username,'Chat')
    if request.session.__contains__('username'):
        status = models.celebrity_chat_start(username)
        if status == True:
            otheruser  = models.celebrity_other_user(username)
            return render(request, 'celibrityhome.html',{'userName': request.session['username'],'datas': list(data),'chatdatas': list(chatdata),'status':status,'otheruser':otheruser})
        return render(request, 'celibrityhome.html',{'userName': request.session['username'],'datas': list(data),'chatdatas': list(chatdata),'status':False})




def request_services(request):
    if request.method == 'POST':
        loginuser = request.POST.get('loginuser', False)
        celebrityname = request.POST.get('celebrityname', False)
        servicetype = request.POST.get('servicetype', False)
        message = request.POST.get('message', False)
        print ('im inisde here**************')
        models.request_model(loginuser, celebrityname, servicetype, message)
        return redirect('homepage')


def upload(request):
    if request.method == 'POST':
        video = request.POST.get('video', False)
        requestuser = request.POST.get('requestuser', False)
        celebrityname = request.POST.get('celebrityname', False)
        models.video_upload(video,requestuser,celebrityname)
        models.video_detail(video, requestuser, celebrityname)
        return redirect('celibrityhome')

def download(request):
    if request.method == 'POST':
        loginuser = request.session['username']
        models.video_download(loginuser)
        return redirect('homepage')


def notification(request):
    if request.session.__contains__('username'):
        uname = request.session['username']
        count = models.notification_count(uname)
        data = models.user_video_info(uname)
        data1 = models.user_chat_info(uname)
        status = models.chat_start(uname)
        if status == True:
            otheruser  = models.other_user(uname)
            return render(request, 'notification.html',{'userName': request.session['username'],'count':count,'datas': list(data),'datas1': list(data1),'status':status,'otheruser':otheruser})
        return render(request, 'notification.html',{'userName': request.session['username'],'count':count,'datas': list(data),'datas1': list(data1),'status':False})

def chattime(request):
    if request.method == 'POST':
        daytime = request.POST.get('daytime', False)
        requestuser = request.POST.get('requestuser', False)
        celebrityname = request.POST.get('celebrityname', False)
        datestring = str(daytime)
        datestring=datestring.replace("T"," ")
        error = models.chat_time(datestring,requestuser,celebrityname)
        return redirect('celibrityhome')


def comment(request):
    if request.method == 'POST':
        loginuser = request.session['username']
        celebrityname = request.POST.get('celebrityname', False)
        message = request.POST.get('message', False)
        models.comment_model(celebrityname,loginuser,message)
        return redirect('homepage')



