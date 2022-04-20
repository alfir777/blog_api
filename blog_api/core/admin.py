from django import forms
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Article, Comment


class ArticleAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.CharField)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    class PostAdmin(admin.ModelAdmin):
        form = ArticleAdminForm


class CommentAdmin(TreeAdmin):
    list_display = ('id', 'article', 'article')

    form = movenodeform_factory(Comment)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
