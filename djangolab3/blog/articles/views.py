from django import template
from .models import Article
from django.shortcuts import render
def archive(request):
	return render(request, 'templates/article.html', {"posts":Article.objects.all()})
