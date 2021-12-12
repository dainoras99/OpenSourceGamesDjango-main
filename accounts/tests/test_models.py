import tempfile
from django.test import Client
from django.test.client import RequestFactory
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from accounts.models import UserGame,NewsClass, Comment, GameComment,Vote,Topic,TopicComment
from accounts.views import comment



class testModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                    username='foo', email='foo@bar', 
                    password='bar')
        self.client.login( username="foo", password="bar")
        self.request = self.factory.get("/my_profile/")
        self.request.user = self.user

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
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            author='waldek2001'
        )

    def test_UserGame_model_str(self):
        self.assertEqual(str(self.testGame.gameName), 'Soldat')
    
    def test_Topic_model_str(self):
        self.assertEqual(str(self.testTopic.topicName), 'Geriausias žaidimas?')

    def test_NewsClass_model_str(self):
        self.assertEqual(str(self.testNews.headline), 'Moksleivis prarado visus pinigus csgo bettinime')
        self.assertEqual(str(self.testNews.author), 'waldek2001')

    def test_Comment_model_str(self):
        testComment = Comment.objects.create( 
            userid=self.request.user,
            newsid=self.testNews,
            body="Geras komentaras!"
        )
        self.assertEqual(str(testComment.userid), self.request.user.username)
        self.assertEqual(str(testComment.newsid.headline), self.testNews.headline)

    def test_GameComment_model_str(self):
        gameComment = GameComment.objects.create( 
            user_id=self.request.user,
            game_id=self.testGame,
            comment_body="Neblogai!"
        )
        self.assertEqual(str(gameComment.user_id), self.request.user.username)
        self.assertEqual(str(gameComment.game_id.gameName), self.testGame.gameName)

    def test_TopicComment_model_str(self):
        topicComment = TopicComment.objects.create( 
            user_id=self.request.user,
            topic_id=self.testTopic,
            comment_body="Neblogai!"
        )
        self.assertEqual(str(topicComment.user_id), self.request.user.username)
        self.assertEqual(str(topicComment.topic_id.topicName), self.testTopic.topicName)
    
    def test_Vote_model_str(self):
        vote = Vote.objects.create( 
            user_id=self.request.user,
            game_id=self.testGame,
            score=37
        )
        self.assertEqual(str(vote.user_id), self.request.user.username)
        self.assertEqual(str(vote.game_id.gameName), self.testGame.gameName)
        self.assertEqual(str(vote.score), '37')

    
    def tearDown(self):
        self.user.delete()
    