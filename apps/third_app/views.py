
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Poke
from django.db.models import Count
from django.contrib import messages
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
        
        return render(request, "third_app/index.html")

def newuser(request):
        if 'id' in request.session:
                # Poke.objects.all().delete()
                user_id = int(request.session['id'])
               
                been_poked = Poke.objects.annotate(Count("poker__id")).filter(poked__id = user_id)

                poked_num = Poke.objects.values("poker__first_name", "poker__last_name").annotate(total=Count("poker")).order_by('total').filter(poked__id = user_id)
 
                context = {
                        "user" : User.objects.get(id = request.session['id']), 
                        "users": User.objects.all().exclude(id = user_id),
                        "pokes": Poke.objects.all(),
                        "been_poked": been_poked,
                        
                        
                        "poked_num" : poked_num

                }
                # print request.session['id']
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
                userpoked = int(request.POST['poked'])
                pokeduser = User.objects.get(id = userpoked)
                print user.first_name
                print userpoked, pokeduser.first_name
                poke = Poke.objects.create(poker = user, poked = pokeduser)
                return redirect ('/newuser')
def logout(request):
        if request.method == "POST":
                request.session.clear()
                return redirect ('/')
        


