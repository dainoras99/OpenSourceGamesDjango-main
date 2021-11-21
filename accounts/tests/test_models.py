from django.test.testcases import TestCase


class testModels(TestCase):

    def setUp(self):
        self.project1=Project.objects.create(
            name='Project 1',
        )