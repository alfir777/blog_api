from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.api import ArticlesViewSet, CommentViewSet, TreeCommentViewSet


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "articles",
                "description": "Методы API для статей"
            },
            {
                "name": "comments",
                "description": "Методы API для комментариев к статьям"
            },
        ]
        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title='Blog API',
        default_version='0.0.1',
        description='Blog API',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('articles/', ArticlesViewSet.as_view()),
    path('comments/', CommentViewSet.as_view()),
    path('comments/tree', TreeCommentViewSet.as_view()),
]
