from django.db import models
from treebeard.mp_tree import MP_Node


class Article(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Title')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_count_comments(self):
        return f"{self.comments.all().count()}"


class Comment(MP_Node):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    node_order_by = ['created', ]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment {self.pk} by "{self.article}'
