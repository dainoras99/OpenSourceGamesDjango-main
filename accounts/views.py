
from django import http
from django.db import connections
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from accounts.models import Comment, Customer, GameComment, UserGame, NewsClass, Vote
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateNewNews, CreateUserForm, CreateNewGame, CreateNewComment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import urllib.request
import json
import requests
from types import SimpleNamespace
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import operator


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
    votes = Vote.objects.all()
    context={'userGame':userGame, 'comment': gameComment, 'votes': votes}
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

def commentGame(request):
     if request.POST.get('action') == 'messagePost':
        id = int(request.POST.get('gameid'))
        message = request.POST.get('message')
        gameObject = UserGame.objects.get(id=id)
        new = GameComment(user_id=request.user, game_id=gameObject, comment_body=message)
        new.save();
        return JsonResponse({'gameid': id, 'message': message, 'userid': request.user.id})


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
    
def scoreGame(request):
     if request.POST.get('action') == 'vote':
        id = int(request.POST.get('gameid'))
        score = int(request.POST.get('score'))
        update = UserGame.objects.get(id=id)
        votesObjects = Vote.objects.filter(game_id=id).all()
        votes = Vote.objects.filter(game_id=id).all().count()
        totalScore=0
        scoreTotal = 0
        for VoteObject in votesObjects:
            scoreTotal = scoreTotal + VoteObject.score
        

        if Vote.objects.filter(user_id=request.user.id, game_id=id).exists():
                q = Vote.objects.get(
                    Q(game_id=id) & Q(user_id=request.user.id))
                evote = q.score
                if evote == score:
                    totalScore = (scoreTotal + score) / votes
                    return JsonResponse({'totalScore':totalScore})
                if evote == 1:
                    print(scoreTotal)
                    update.score = ((scoreTotal - 1) + score) / votes
                    totalScore = (scoreTotal + score) / votes
                    update.save()
                    print((scoreTotal + score) / votes)
                    q.delete()
                    new = Vote(user_id=request.user, game_id=update, score=score)
                    new.save()
                    update.refresh_from_db()
                    return JsonResponse({'totalScore':totalScore})
                if evote == 2:
                    update.score = ((scoreTotal - 2) + score) / votes
                    totalScore = (scoreTotal + score) / votes
                    update.save()
                    print((scoreTotal + score) / votes)
                    q.delete()
                    new = Vote(user_id=request.user, game_id=update, score=score)
                    new.save()
                    update.refresh_from_db()
                    return JsonResponse({'totalScore':totalScore})
                if evote == 3:
                    update.score = ((scoreTotal - 3) + score) / votes
                    totalScore = (scoreTotal + score) / votes
                    update.save()
                    print((scoreTotal + score) / votes)
                    q.delete()
                    new = Vote(user_id=request.user, game_id=update, score=score)
                    new.save()
                    update.refresh_from_db()
                    return JsonResponse({'totalScore':totalScore})
                if evote == 4:
                    update.score = ((scoreTotal - 4) + score) / votes
                    totalScore = (scoreTotal + score) / votes
                    update.save()
                    print((scoreTotal + score) / votes)
                    q.delete()
                    new = Vote(user_id=request.user, game_id=update, score=score)
                    new.save()
                    update.refresh_from_db()
                    return JsonResponse({'totalScore':totalScore})
                if evote == 5:
                    update.score = ((scoreTotal - 5) + score) / votes
                    totalScore = (scoreTotal + score) / votes
                    update.save()
                    print((scoreTotal + score) / votes)
                    q.delete()
                    new = Vote(user_id=request.user, game_id=update, score=score)
                    new.save()
                    update.refresh_from_db()
                    return JsonResponse({'totalScore':totalScore})

        update.score = (scoreTotal + score) / (votes + 1)
        update.save()
        new = Vote(user_id=request.user, game_id=update, score=score)
        new.save()

        update.refresh_from_db()
        up = update.score
        return JsonResponse({'score':score, 'up':up})
