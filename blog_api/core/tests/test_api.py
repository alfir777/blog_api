from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from core.models import Article
from core.serializers import ArticleSerializer

factory = APIRequestFactory()


class ArticleTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(title='Test')
        cls.article1 = Article.objects.create(title='Test 1')

    def test_get_articles(self):
        response = self.client.get('/articles/')
        serializer_data = ArticleSerializer([self.article, self.article1], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data, response.data)

    def test_post_articles(self):
        response = self.client.post('/articles/?title=Test 2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
