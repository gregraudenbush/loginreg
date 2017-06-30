
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote, Favorite
from django.db.models import Count
from django.contrib import messages
import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
        # Quotes.objects.all().delete()
        # Favorites.objects.all().delete()
        return render(request, "third_app/index.html")

def addquote(request):
        if 'id' in request.session:
                # Poke.objects.all().delete()
                user_id = int(request.session['id'])
               
                # been_poked = Poke.objects.annotate(Count("poker__id")).filter(poked__id = user_id)

                # poked_num = Poke.objects.values("poker__first_name", "poker__last_name").annotate(total=Count("poker")).order_by('total').filter(poked__id = user_id)
                # "quotes" : Quote.objects.all().exclude(quote1 = Favorite.objects.get(quote__quote = quote__quote1))
                
                
                favorite_id = Favorite.objects.values("quote__id").values("quote")


                context = {
                        "user" : User.objects.get(id = request.session['id']), 
                        "quotes" : Quote.objects.all().exclude(id = Favorite.objects.all().values("quote__id")),
                        "favorites" : Favorite.objects.filter(user = User.objects.get(id = request.session['id'])),
                        "user_id" : int(request.session['id'])
                }
                
                return render(request, "third_app/addquote.html", context)

                
        return redirect('/')


def login(request):
        if request.method =="POST":
                login = User.objects.login(request.POST)
                if login['status']:                
                        request.session['id'] = login['data'].id
                        return redirect('/addquote')
                else:
                        messages.error(request, "Email or password invalid")
        return redirect('/')        

def val(request):
        if request.method == "POST":
                res = User.objects.val(request.POST)
                if res['status']:
                        messages.success(request, "Thank You For Registering")
                        request.session['id'] = res['data'].id
                        return redirect('/addquote')
                else:
                        for errors in res['data']:
                                messages.error(request, errors)
        return redirect('/')
def add(request):

        if request.method == "POST":
                # quote = Quote.objects.add(request.POST)
                user = User.objects.get(id = request.session['id'])
                quote1 = str(request.POST['quote1'])
                author1 = str(request.POST['author'])
                if len(quote1) < 1 or len(author1) < 1:
                        messages.error(request, "Please Complete The Form")
                        return redirect('/addquote')
                else:
                        Quote.objects.create(user = User.objects.get(id = request.session['id']), quote1 = quote1, author = author1)
                        messages.success(request, "Thanks for adding a quote!")
                        return redirect('/addquote')

                # if quote['status']:
                #         messages.success(request, "Thanks for adding a quote!")
                #         return redirect('/addquote')
                # else:
                #         for errors in quote['data']:
                #                 messages.error(request, errors) 

                #         return redirect('/addquote')

def favorite(request):

        if request.method == "POST":
                Favorite.objects.create(quote = Quote.objects.get(id = request.POST['quote_id']), user = User.objects.get(id = request.session['id']))
                
        return redirect ('/addquote')

def removefavorite(request):
        
        if request.method == "POST":
                Favorite.objects.get(id = request.POST['id']).delete()
                
        return redirect ('/addquote')  

def user (request, id):
    user = User.objects.get(id = id)
    count = Quote.objects.filter(user = user).count()
    context = {
        "user" : User.objects.get(id = id),
        "quotes" : Quote.objects.filter(user = user),
        "count" : count
    }

    return render(request, "third_app/user.html", context)



                       
def logout(request):
        if request.method == "POST":
                request.session.clear()
                return redirect ('/')    
# def poke(request):
#         if request.method == "POST":
#                 user = User.objects.get(id = request.session['id'])
#                 userpoked = int(request.POST['poked'])
#                 pokeduser = User.objects.get(id = userpoked)
#                 print user.first_name
#                 print userpoked, pokeduser.first_name
#                 poke = Poke.objects.create(poker = user, poked = pokeduser)
#                 return redirect ('/newuser')
# def logout(request):

#         if request.method == "POST":
#                 request.session.clear()
#                 return redirect ('/')
        


