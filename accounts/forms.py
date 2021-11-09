from django import forms
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import  Comment, NewsClass, UserGame

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        

class CreateNewGame(ModelForm):
    class Meta:
        model=UserGame
        fields=['gameName','gameDescription','gameCode', 'image','gameOwnerUsername']

class CreateNewNews(ModelForm):
    class Meta:
        model=NewsClass
        fields=['headline','author','text', 'image']

class CreateNewComment(ModelForm):
    class Meta:
        model=Comment
        fields=['userid','newsid','body']
       


