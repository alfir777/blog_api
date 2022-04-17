from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Article(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Title')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    def get_count_comments(self):
        return f"{self.comments.all().count()}"


class Comment(MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=False)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        return f'Comment {self.pk} by "{self.article}'
