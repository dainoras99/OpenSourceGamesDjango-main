from django.test import TestCase, Client, client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserGame,NewsClass,Comment, GameComment,Vote,Topic,TopicComment
import tempfile
from django.test.client import RequestFactory 
import random


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                    username='foo', email='foo@bar', 
                    password='bar')

        self.testGame = UserGame.objects.create(
            gameName="Soldat",
            gameDescription="Pirma šaudyklė, puikus žaidimas.",
            gameCode="<<helloWorld>>",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

        self.testTopic = Topic.objects.create(
            topicName="Geriausias žaidimas?",
            topicDescription="Koks geriausias žaidimas šiuo metu?"
        )

        self.testNews = NewsClass.objects.create(
            headline="Moksleivis prarado visus pinigus csgo bettinime",
            text="rip pinigeliai",
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_news_GET(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/news.html')

    def test_topics_GET(self):
        response = self.client.get(reverse('topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/forum.html')

    def test_register_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_games_GET(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/games.html')
    
    def test_uploadGame_POST(self):
        response = self.client.post(reverse('uploadGame'), {
            'gameName': 'Soldati periot',
            'gameDescription': 'Nice',
            'gameCode': 'Hello world'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/uploadGame.html')

    def test_uploadNews_POST(self):
        response = self.client.post(reverse('uploadNews'), {
            'headline': 'Įspėja dėl pavojingo viruso plitimo: užkibę ant kabliuko gali skaudžiai nukentėti',
            'text': 'Skandinavai perspėja apie trumposiomis žinutėmis telefonuose plintantį virusą Flubot.'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/uploadNews.html')
    
    def test_uploadTopic_POST(self):
        response = self.client.post(reverse('uploadTopic'), {
            'topicName': 'Geriausias zaidimas Lietuvoje?',
            'topicDescription': 'Ka mastot, zmones?'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/uploadTopic.html')
    
    def test_gamesPage_GET(self):
         response = self.client.get(reverse('gamesPage', args=[self.testGame.id]))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'accounts/gamesPage.html')

    def test_newsPage_GET(self):
         response = self.client.get(reverse('newsPage', args=[self.testNews.id]))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'accounts/newsPage.html')

    def test_topicPage_GET(self):
         response = self.client.get(reverse('topicPage', args=[self.testTopic.id]))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'accounts/forumPage.html')

    def test_commentGame_POST(self):
        self.client.login( username="foo", password="bar")
        request = self.factory.get("/my_profile/")
        request.user = self.user

        response = self.client.post(reverse('commentGame'), {
            'gameid': self.testGame.id,
            'action': 'messagePost',
            'message': 'Geras Zaidimas.'
        })

        self.assertEqual(GameComment.objects.all().count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_commentGame_POST(self):
        self.client.login( username="foo", password="bar")
        request = self.factory.get("/my_profile/")
        request.user = self.user

        response = self.client.post(reverse('commentTopic'), {
            'topicid': self.testTopic.id,
            'action': 'messagePost',
            'message': 'Geriausias zaidimas yra minecraftas, waldekas sake)).'
        })

        self.assertEqual(TopicComment.objects.all().count(), 1)
        self.assertEqual(TopicComment.objects.all().first().comment_body, 
        'Geriausias zaidimas yra minecraftas, waldekas sake)).')
        self.assertEqual(response.status_code, 200)

    def test_comment_POST(self):
        self.client.login( username="foo", password="bar")
        request = self.factory.get("/my_profile/")
        request.user = self.user
        
        response = self.client.post(reverse('comment'), {
            'newsid': self.testNews.id,
            'action': 'messagePost',
            'message': 'Neblogai cia, rip pinigeliai'
        })

        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.all().first().body, 'Neblogai cia, rip pinigeliai')
        self.assertEqual(response.status_code, 200)
    
    def test_comment_POST(self):
        self.client.login( username="foo", password="bar")
        request = self.factory.get("/my_profile/")
        request.user = self.user
        randomScore = random.randint(1, 5)

        response = self.client.post(reverse('scoreGame'), {
            'gameid': self.testGame.id,
            'action': 'vote',
            'score': str(randomScore)
        })
        self.assertEqual(Vote.objects.all().count(), 1)
        self.assertEqual(Vote.objects.all().first().score, randomScore)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.user.delete()