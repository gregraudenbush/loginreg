
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
        
        # User.objects.all().delete()

        return render(request, "third_app/index.html")

def login(request):
        
        if request.method =="POST":
                
                login = User.objects.login(request.POST['email'], request.POST['password'])
        
        if login['status']:
            
            success = login['data']
        #     messages.error(request, success[0])
            user = User.objects.get(email = request.POST['email'])
            request.session['id'] = user.id
            return redirect('/newuser')

        else:
            error = login['data']
            messages.success(request, error[0])
            return redirect('/')
def newuser(request):
        context = {
                "name2" : User.objects.get(id = request.session['id'])
        }

        return render(request, "third_app/newuser.html", context)
def val(request):
        if request.method == "POST":
                
                res = User.objects.val(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['password2'])

        if res['status']:
            
            username = res['data'].first_name
            messages.success(request, "Thank You For Registering")
            user = User.objects.get(email = request.POST['email'])
            request.session['id'] = user.id
            return redirect('/newuser')
        else:
            for errors in res['data']:
                messages.error(request, errors)
            return redirect('/')
        
     
        


