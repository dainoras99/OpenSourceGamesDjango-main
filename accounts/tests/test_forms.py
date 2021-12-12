from io import BytesIO
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from django.forms.fields import ImageField
from django.test import TransactionTestCase
from accounts.forms import CreateUserForm, CreateNewGame, CreateNewNews, CreateNewTopic, CreateNewComment
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from accounts.models import NewsClass

class TestForms(TransactionTestCase):

    def test_CreateUserForm_valid_data(self):
        form = CreateUserForm(data={
            'username': 'waldek',
            'email': 'waldek2001@gmail.com',
            'password1': 'geras_sabaka',
            'password2': 'geras_sabaka'
        })

        self.assertTrue(form.is_valid())

    def test_CreateUserForm_invalid_data(self):
        form = CreateUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_CreateNewGame_invalid_data(self):
        loaded_file = BytesIO(b"some dummy bcode data: \x00\x01")
        loaded_file.name = 'test_file_name.jpg'

        data={
            'gameName':'Soldat',
            'gameDescription':'Geras zaidimas',
            'gameCode':'Hello world',
            'gameOwnerUsername':'waldek2001'
        }
        file_dict = {'image': SimpleUploadedFile(loaded_file.name, loaded_file.read())}
        form=CreateNewGame(data=data, files=file_dict)
        self.assertFalse(form.is_valid())

    def test_CreateNewNews_invalid_data(self):
        loaded_file = BytesIO(b"some dummy bcode data: \x00\x01")
        loaded_file.name = 'test_file_name.jpg'

        data={
            'headline':'Gera naujiena',
            'author':'waldek',
            'text':'Hello world'
        }
        file_dict = {'image': SimpleUploadedFile(loaded_file.name, loaded_file.read())}
        form=CreateNewNews(data=data, files=file_dict)
        self.assertFalse(form.is_valid())

    def test_CreateNewTopic_valid_data(self):
        data={
            'topicName':'Geras',
            'user_id':'waldek',
            'topicDescription':'Hello world'
        }
        form=CreateNewTopic(data=data)
        self.assertTrue(form.is_valid())

    def test_CreateNewTopic_invalid_data(self):
        data={}
        form=CreateNewTopic(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_CreateNewComment_valid_data(self):
        user = User.objects.create_user(
                    username='foo', email='foo@bar', 
                    password='bar')
        news = NewsClass.objects.create(
            headline="Moksleivis prarado visus pinigus csgo bettinime",
            text="rip pinigeliai",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        data={
            'userid': user,
            'newsid': news,
            'body':'Hello world'
        }
        form=CreateNewComment(data=data)
        self.assertTrue(form.is_valid())
    # coverage run --branch --source=accounts ./manage.py test
    