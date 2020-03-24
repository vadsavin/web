from django import template
from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404

def archive(request):
	return render(request, 'templates/archive.html', {"posts":Article.objects.all()})

def get_article(request, article_id):
	try:
		post = Article.objects.get(id=int(article_id))
		return render(request, 'article.html', {"post": post})
	except Article.DoesNotExist:
		raise Http404

def create_post(request):
	if not request.user.is_anonymous:
		if request.method == "POST":
			form = {
		 		'text' : request.POST["text"], 
		 		'title': request.POST["title"],
		 	}

			articles = set(Article.objects.all())
			titles = []
			for a in articles:
				titles.append(a.title)
			
			if not (form["text"] and form["title"]):
				form['errors'] = u"Не все поля заполнены!"
				return render(request, 'create_post.html',{'form': form})
			elif form["title"] in titles:
				form['errors'] = u"Заголовок статьи не уникален!"
				return render(request, 'create_post.html',{'form': form})
			else:
				article = Article.objects.create(text=form["text"],title=form["title"], author=request.user)
				return redirect('get_article', article_id=article.id)
		else:
 			# просто вернуть страницу с формой, если метод GET
 			return render(request, 'create_post.html', {})
	else:
		raise Http404