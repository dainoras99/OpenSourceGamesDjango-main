
from django import http
from django.db import connections
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from accounts.models import Comment, Customer, GameComment, UserGame, NewsClass
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateNewNews, CreateUserForm, CreateNewGame, CreateNewComment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import urllib.request
import json
import requests
from types import SimpleNamespace

# Create your views here.
def home(request):
    news= NewsClass.objects.all()
    return render(request,'accounts/index.html',{'news':news})

def news(request):

    news= NewsClass.objects.all()
    return render(request,'accounts/news.html',{'news':news})

def register(request):
    form= CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            # username=form.cleaned_data.get('username')
            # messages.success(request, 'Paskyra sukurta '+ username)
            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user=authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Slapyvardis arba slaptazodis neteisingas!')
    return render(request,'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('home')

def games(request):

    userGame= UserGame.objects.all()
    return render(request,'accounts/games.html',{'userGame':userGame})

def gamesPage(request,pk):
    gameComment = GameComment.objects.all()
    userGame= UserGame.objects.get(id=pk)
    context={'userGame':userGame, 'comment': gameComment}
    return render(request,'accounts/gamesPage.html',context)

def uploadGame(request):
    form=CreateNewGame()
    uloggedinuser=request.user.username
    form = CreateNewGame(initial={'gameOwnerUsername': uloggedinuser})
    if request.method=='POST':
        form=CreateNewGame(request.POST, request.FILES)
        print(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('games')
    context={'form':form}

    return render(request,'accounts/uploadGame.html',context)


def newsPage(request,pk):
    news=NewsClass.objects.get(id=pk)
    comment=Comment.objects.all()
    context={'news':news, 'comment':comment}
    return render(request,'accounts/newsPage.html',context)

    

def uploadNews(request):
    form=CreateNewNews()
 
    if request.method=='POST':
        form=CreateNewNews(request.POST, request.FILES)
        print(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('news')
    context={'form':form}
    return render(request,'accounts/uploadNews.html',context)

def comment(request):
    # form=CreateNewComment()
    # news=NewsClass.objects.get(id=pk)
    # print(news.headline)
    # form = CreateNewComment(initial={'userid': request.user.id, 'newsid':news.id})
    # if request.method=='POST':
    #     form=CreateNewComment(request.POST,)
    #     print(request.POST)
        
    #     if(form.is_valid()):
    #         form.save()
    #         return redirect('news')
    
    # context={'form':form}
    # return render(request,'accounts/addComment.html',context)
    if request.POST.get('action') == 'messagePost':
        id = int(request.POST.get('newsid'))
        message = request.POST.get('message')
        newsObject = NewsClass.objects.get(id=id)
        new = Comment(userid=request.user, newsid=newsObject, body=message)
        new.save();
        return JsonResponse({'newsid': id, 'message': message, 'userid': request.user.id})

    
def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
  
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' 
                    +city +'&units=metric'+'&appid=92285950c1c416ae4e085529b9363334').read()
  
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
  
        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data ={}
    return render(request, "accounts/weatherPage.html", data)

def covid(request):
    url = "https://covid-19-data.p.rapidapi.com/country/code"

    querystring = {"code":"lt"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "b581c6a1b8msh4e278cd97a01bf3p15e37djsn7ad0816b556d"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    list_of_data = json.loads(response.text)
    data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
    
    print(data)

    # return render(request, "accounts/weatherPage.html")
    
def gamesapi(request):
    response=requests.get('https://www.freetogame.com/api/games')
    data= response.json()
    
    return render(request, "accounts/gamesAPI.html",{'response':data})
    
