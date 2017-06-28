
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Poke
from django.contrib import messages
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
        # User.objects.all().delete()
        Poke.objects.all().delete()
        return render(request, "third_app/index.html")

def newuser(request):
        if 'id' in request.session:
                # Poke.objects.all().delete()
                context = {
                        "user" : User.objects.get(id = request.session['id']), 
                        "users": User.objects.all(),
                        "pokes": Poke.objects.all()
                        
                }
                print request.session['id']
                return render(request, "third_app/newuser.html", context)

                print users
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
        
def poke(request):
        if request.method == "POST":
                user = User.objects.get(id = request.session['id'])
                userpoked = request.POST['userpoked']
                poke = Poke.objects.create(user = User.objects.get(id = request.session['id']), userpoked = User.objects.get(id = request.POST['userpoked']))
                return redirect ('/newuser')
def logout(request):
        if request.method == "POST":
                request.session.clear()
                return redirect ('/')
        


