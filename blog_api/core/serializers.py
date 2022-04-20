from rest_framework import serializers

from .models import Article


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    article_id = serializers.IntegerField()
    created = serializers.DateTimeField(format='%m-%d-%y %H:%M:%S')
    content = serializers.CharField()
    path = serializers.IntegerField()


class ArticleSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='get_count_comments', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'comments_count']
