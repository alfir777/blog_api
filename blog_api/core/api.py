from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Article
from .serializers import ArticleSerializer, TreeCommentsSerializer, CommentSerializer, TreeCommentSerializer


class ArticlesViewSet(APIView):
    serializer_class = ArticleSerializer

    @swagger_auto_schema(
        methods=['POST', ],
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="title article", type=openapi.TYPE_STRING,
                              required=True)
        ],
        operation_summary='Создание статьи',
        tags=['articles', ],
    )
    @action(detail=False, methods=['POST', ])
    def post(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        article = Article(title=title)
        article.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=201)

    @swagger_auto_schema(
        methods=['GET', ],
        operation_summary='Список статей с комментариями',
        tags=['articles', ],
    )
    @action(detail=False, methods=['GET', ])
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(APIView):
    @swagger_auto_schema(
        methods=['POST', ],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="id article", type=openapi.TYPE_INTEGER,
                              required=True),
            openapi.Parameter('content', openapi.IN_QUERY, description="text comment", type=openapi.TYPE_STRING,
                              required=True),
        ],
        operation_summary='Создание комментария к статье',
        tags=['comments', ],
    )
    @action(detail=False, methods=['POST', ])
    def post(self, request, *args, **kwargs):
        try:
            queryset = Comment(article=Article.objects.get(id=request.query_params.get('id')),
                               content=request.query_params.get('content'))
            queryset.save()
        except ObjectDoesNotExist:
            response = {
                'info': 'Данной статьи не существует'
            }
            return JsonResponse(response, status=404)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data, status=201)

    @swagger_auto_schema(
        methods=['GET', ],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="id комментария", type=openapi.TYPE_INTEGER,
                              required=True)
        ],
        operation_summary='Список комментариев комментария',
        tags=['comments', ],
    )
    @action(detail=False, methods=['GET', ])
    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.filter(parent=Comment.objects.get(id=request.query_params.get('id')))
        serializer = TreeCommentSerializer(queryset, many=True)
        return Response(serializer.data)


class TreeCommentViewSet(APIView):
    @swagger_auto_schema(
        methods=['POST', ],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="id комментария", type=openapi.TYPE_INTEGER,
                              required=True),
            openapi.Parameter('content', openapi.IN_QUERY, description="текст комментария", type=openapi.TYPE_STRING,
                              required=True),
        ],
        operation_summary='Создание комментария к комментарию',
        tags=['comments', ],
    )
    @action(detail=False, methods=['POST', ])
    def post(self, request, *args, **kwargs):
        try:
            parent = Comment.objects.get(id=request.query_params.get('id'))
        except ObjectDoesNotExist:
            response = {
                'error': 'Данного комментария не существует'
            }
            return JsonResponse(response, status=404)
        comment = Comment(article=parent.article,
                          content=request.query_params.get('content'),
                          parent=parent)
        comment.save()
        serializer = CommentSerializer(comment, many=False)
        return JsonResponse(serializer.data, status=201)

    @swagger_auto_schema(
        methods=['GET', ],
        operation_summary='Список всех комментариев',
        tags=['comments', ],
    )
    @action(detail=False, methods=['GET', ])
    def get(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = TreeCommentsSerializer(queryset, many=True)
        return Response(serializer.data)
