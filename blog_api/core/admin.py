from django import forms
from django.contrib import admin

from .models import Article, Comment


class ArticleAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.CharField)

    class Meta:
        model = Article
        fields = '__all__'


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    class PostAdmin(admin.ModelAdmin):
        form = ArticleAdminForm


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'article', 'parent')

    form = CommentAdminForm


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
