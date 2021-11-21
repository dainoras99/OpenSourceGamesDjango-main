from django.test import TestCase, Client, client
from django.urls import reverse
from accounts.models import Customer, UserGame,NewsClass,Comment, GameComment,Vote,Topic,TopicComment
import json


class TestView(TestCase):
    def test_home_GET(self):
        client= Client()
        response= client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_news_GET(self):
        client= Client()
        response= client.get(reverse('news'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/news.html')

    def test_topics_GET(self):
        client= Client()
        response= client.get(reverse('topics'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/forum.html')

    def test_register_GET(self):
        client= Client()
        response= client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_GET(self):
        client= Client()
        response= client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_games_GET(self):
        client= Client()
        response= client.get(reverse('games'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/games.html')
    
    # def test_gamesPage_GET(self):
    #     client= Client()
    #     response= client.get(reverse('gamesPage',args=[5]))

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'accounts/gamesPage.html')

    # def test_topicPage_GET(self):
    #     client= Client()
    #     response= client.get(reverse('topicPage',args=[4]))

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'accounts/forumPage.html')