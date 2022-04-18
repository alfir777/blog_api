from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from core.models import Article, Comment
from core.serializers import ArticleSerializer, TreeCommentSerializer

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


class CommentTest(APITestCase):
    article1 = None
    article = None

    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(title='Test')
        cls.article1 = Article.objects.create(title='Test 1')
        cls.comment = Comment.objects.create(article=cls.article, content='Comment')
        cls.comment1 = Comment.objects.create(article=cls.article1, content='Comment 1')

    def test_get_comments(self):
        response = self.client.get('/comments/tree')
        serializer_data = TreeCommentSerializer([self.comment1, self.comment], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data, response.data)

    def test_post_comments(self):
        response = self.client.post('/comments/?id=1&content=Comment 2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comment(self):
        comment2 = Comment.objects.create(article=self.article1, content='Comment 2', parent=self.comment)
        response = self.client.get('/comments/?id=1')
        serializer_data = TreeCommentSerializer([comment2, ], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_post_comments_tree(self):
        response = self.client.post('/comments/tree?id=1&content=Comment 3')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
