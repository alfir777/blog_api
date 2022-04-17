from rest_framework import serializers

from .models import Comment, Article


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveCommentSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent']


class TreeCommentsSerializer(serializers.ModelSerializer):
    children = RecursiveCommentSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'children']


class TreeCommentSerializer(serializers.ModelSerializer):
    children = RecursiveCommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', 'parent', 'children']


class ArticleSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='get_count_comments', read_only=True)
    comments = TreeCommentsSerializer(many=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'comments_count', 'comments']
