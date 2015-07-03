#coding:utf-8
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context,RequestContext
from django.template.context_processors import csrf
from django.http.response import HttpResponse, HttpResponseRedirect
from DjangoCaptcha import Captcha
import httplib, urllib
import random
debug = 1
def login(request):
    c= {}
    errCode = -1
    username=""
    password=""
    c.update(csrf(request))
     
    if request.method == 'POST':
        checkcode = request.POST.get('checkcode','')
        ca = Captcha(request)
        if not ca.check(checkcode):
            errCode = -2
        else:
            username = request.POST.get('name','')
            password = request.POST.get('uPassword', '')
            user = auth.authenticate(username=username,password=password)
            if user and user.is_active:
                auth.login(request,user)
                errCode = 0
            else:
                errCode = -3
    else:
        print("GET WAY")
    
    if debug:
        print("UserName : %s"%username)
        print("Password : %s"%password)
        print("errCode  : %d"%errCode)    

    if errCode == 0:
        html = render(request, 'login_success.html', c)
    else:
        html = render(request, 'login_fail.html',c)
    return HttpResponse(html)

def logout(request):
    print("Logout")
    
def register(request):
    html = render(request,'register.html')
    return HttpResponse(html)

def sendsms(request):
    csrftoken = request.COOKIES['csrftoken'];

    mobile = request.GET.get('mobile',"")
    smscode = "%4d"%random.randint(0,9999)
    content="您的验证码是：%s。请不要把验证码泄露给其他人。"%smscode
    if debug:
        print("csrftoken: %s"%csrftoken)
        print("mobile: %s"%mobile)
        print("code: %s"%smscode)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    data = urllib.urlencode({"account" : "cf_cat",
            "password" : "zhangbo123", # the password should be "zhangbo"
            "mobile" : mobile,
            "content" : content,
            })
    httpClient = httplib.HTTPConnection('106.ihuyi.cn', 80, False, 30)
    httpClient.request('POST', '/webservice/sms.php?method=Submit', data, headers)
    httpres = httpClient.getresponse()
    print httpres.status
    print httpres.reason
    print httpres.read()
    return HttpResponse(httpres.status)
def registerHandler(request):
    c= {}
    errCode = -1
    c.update(csrf(request))
    print("path: %s"%request.path)
    print("host: %s"%request.get_host())
    print("user")
    print(request.user)
    if request.user.is_authenticated(): 
        print("Already login")
        auth.logout(request)
        return HttpResponseRedirect("login_success")  
    try:
        if request.method=='POST':  
            username=request.POST.get('name','')  
            password=request.POST.get('uPassword','')  
            email=request.POST.get('email','')  
            phone=request.POST.get('phone','')  
            errors=[]  
            if debug:
                print("UserName : %s"%username)
                print("Password : %s"%password)  
            filterResult=User.objects.filter(username=username)  
            if len(filterResult)>0:  
                errors.append("用户名已存在")  
                return render(request, "register_fail.html")  
              
            newuser = User.objects.create_user(username, email,password)
            newuser.save()  
                
            #登录前需要先验证  
            user = auth.authenticate(username=username,password=password)  
            if user is not None:  
                auth.login(request, user)#g*******************  
                return HttpResponseRedirect("register_success.html") 
            else:
                print("register success")
    except Exception,e:  
        print("exception: %s"%str(e))
        errors.append(str(e))  
        return render(request,"register_fail.html")  
        

'''
登陆验证码生成函数，具体实现和改进参考/usr/local/lib/python2.7/dist-packages/DjangoCaptcha
'''
def captcha(request):
    ca =  Captcha(request)
    ca.words = ['a','b','c']
    ca.type = 'number'
    #ca.type = 'word'
    return ca.display()
    
