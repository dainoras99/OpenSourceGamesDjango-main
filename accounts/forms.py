from django import forms
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import  Comment, NewsClass, Topic, UserGame

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels = {
            'username': 'Vartotojo vardas',
            'email': 'El.Paštas',
            'password1': 'Slaptažodis',
            'password2': 'Pakartokite slaptažodį',
        }

class CreateNewGame(ModelForm):
    class Meta:
        model=UserGame
        fields=['gameName','gameDescription','gameCode', 'image','gameOwnerUsername']
        labels = {
            'gameName': 'Žaidimo pavadinimas',
            'gameDescription': 'Žaidimo aprašymas',
            'gameCode': 'Žaidimo kodas',
            'image': 'Žaidimo nuotraukos įkelimas',
        }
        widgets={
            'gameDescription' : forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'gameCode' : forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        }
        
        

class CreateNewNews(ModelForm):
    class Meta:
        model=NewsClass
        fields=['headline','author','text', 'image']
        labels = {
            'headline': 'Antraštė',
            'author': 'Autorius',
            'text': 'Naujiena',
            'image': 'Naujienos nuotrauka',
        }
        widgets={
            'text' : forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }

class CreateNewTopic(ModelForm):
    class Meta:
        model=Topic
        fields=['topicName','user_id','topicDescription']
        labels = {
            'topicName': 'Antraštė',
            'user_id': 'Autorius',
            'topicDescription': 'Diskusija',
        }
        widgets={
            'topicDescription' : forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }

class CreateNewComment(ModelForm):
    class Meta:
        model=Comment
        fields=['userid','newsid','body']
       


