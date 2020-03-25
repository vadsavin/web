from django import template
from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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


def register(request):
	
	form = {
		'name' : request.POST.get('name'),
		'email': request.POST.get('email'),
		'pass' : request.POST.get('pass'),
	}
	#print(form)
	if not (form['name'] and form['email'] and form['pass']):
		form['errors'] = u"Не все поля заполнены!"
		return render(request, 'register.html',{'form': form})
	else:
		try:
			u = User.objects.get(username=form['name'])
			form['errors'] = u'Пользователь с таким именем уже существует'
			return render(request, 'register.html',{'form': form})
		except:
			User.objects.create_user(form['name'],form['email'],form['pass'])
			form['errors'] = u'Успешная регистрация'
			return render(request, 'register.html',{'form': form})

def auth(request):
	form = {
		'name' : request.POST.get('name'),
		'pass' : request.POST.get('pass'),
	}
	#print(form)
	if not (form['name'] and form['pass']):
		form['errors'] = u"Не все поля заполнены!"
		return render(request, 'auth.html',{'form': form})
	else:
		user = authenticate(username=form['name'], password=form['pass'])
		if not user:
			form['errors'] = u'Неверный логин или пароль'
		else:
			login(request, user)
			form['errors'] = u'Вы вошли как '+user.username
		return render(request, 'auth.html',{'form': form})
			