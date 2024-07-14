from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from article.models import Article


class ArticleListView(ListView):
    template_name = "article/article.html"
    model = Article
    paginate_by = 8


class ArticleDetail(DetailView):
    model = Article




