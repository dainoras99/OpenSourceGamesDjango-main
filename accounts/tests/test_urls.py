from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import home,news,register,login,logout,games,gamesPage,uploadGame,newsPage,comment,weather,covid,gamesapi,scoreGame,commentGame,topics,topicPage,commentTopic,uploadTopic

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertTrue(resolve(url).func,home)

    def test_news_url_is_resolved(self):
        url = reverse('news')
        self.assertTrue(resolve(url).func,news)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertTrue(resolve(url).func,register)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertTrue(resolve(url).func,login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertTrue(resolve(url).func,logout)

    def test_games_url_is_resolved(self):
        url = reverse('games')
        self.assertTrue(resolve(url).func,games)

    def test_gamesPage_url_is_resolved(self):
        url = reverse('gamesPage',args=[1])
        self.assertTrue(resolve(url).func,gamesPage)

    def test_uploadGame_url_is_resolved(self):
        url = reverse('uploadGame')
        self.assertTrue(resolve(url).func,uploadGame)

    def test_postComment_url_is_resolved(self):
        url = reverse('comment')
        self.assertTrue(resolve(url).func,comment)

    def test_weather_url_is_resolved(self):
        url = reverse('weather')
        self.assertTrue(resolve(url).func,weather)

    def test_covid_url_is_resolved(self):
        url = reverse('covid')
        self.assertTrue(resolve(url).func,covid)

    def test_gamesapi_url_is_resolved(self):
        url = reverse('gamesapi')
        self.assertTrue(resolve(url).func,gamesapi)

    def test_scoreGame_url_is_resolved(self):
        url = reverse('scoreGame')
        self.assertTrue(resolve(url).func,scoreGame)

    def test_postCommentGame_url_is_resolved(self):
        url = reverse('commentGame')
        self.assertTrue(resolve(url).func, commentGame)

    def test_forum_url_is_resolved(self):
        url = reverse('topics')
        self.assertTrue(resolve(url).func, topics)

    def test_topicPage_url_is_resolved(self):
        url = reverse('topicPage',args=[5])
        self.assertTrue(resolve(url).func,topicPage)

    def test_postCommentTopic_url_is_resolved(self):
        url = reverse('commentTopic')
        self.assertTrue(resolve(url).func, commentTopic)

    def test_uploadTopic_is_resolved(self):
        url = reverse('uploadTopic')
        self.assertTrue(resolve(url).func, uploadTopic)







  
    