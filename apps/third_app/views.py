
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
        return render(request, "third_app/index.html")

def newuser(request):
        if 'id' in request.session:
                context = {
                        "user" : User.objects.get(id = request.session['id'])
                }
                return render(request, "third_app/newuser.html", context)
        return redirect('/')


def login(request):
        if request.method =="POST":
                login = User.objects.login(request.POST)
                if login['status']:                
                        request.session['id'] = login['data'].id
                        return redirect('/newuser')
                else:
                        messages.error(request, "Email or password invalid")
        return redirect('/')        

def val(request):
        if request.method == "POST":
                res = User.objects.val(request.POST)
                if res['status']:
                        messages.success(request, "Thank You For Registering")
                        request.session['id'] = res['data'].id
                        return redirect('/newuser')
                else:
                        for errors in res['data']:
                                messages.error(request, errors)
        return redirect('/')
        
     
        


