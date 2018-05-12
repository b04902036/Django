# Django
Since Django has updated to version 2.0, there are several new stuff make creating a website more efficiently and securely, I decide to make a quick document of a HOWTO, and a tutorial_site demonstrate the following tutorial
 - [Django official guide](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
 - [install and version clarification](#install-and-version-clarification)
 - [create a Django project](#create-a-django-project)
 - [create a Django app](#create-a-django-app)
 - [make a successful url request](#make-a-successful-url-request)
 - [add model to sql](#add-model-to-sql)
 - [add template](#add-template)
 - [add form](#add-form)
## install and version clarification
I am using python 3.6.0 and django 2.0.5 on windows 10
```
pip install django==2.0.5
```
## create a Django project
```
# start a new project with name NAME, I use "tutorial_site" here
django-admin startproject tutorial_site
# create a superuser
cd tutorial_site
python manage.py createsuperuser
# remember your account and pwd !
```
  created tree structure
```
tutorial_site/
    manage.py
    tutorial_site/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```
 - the outer tutorial_site
    - can be renamed, only a folder containing the project
 - manage.py
    - used to interact with the project, e.g.```python manage.py runserver 8080```
 - __init__.py
    - make this directory a python package
 - settings.py
    - well documented file, used to config this project, e.g. time zone, add new app
 - urls.py
    - add new url mapping
 - wsgi.py
    - see [here](https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/) for more details
 ## create a Django app
 ```
 # start a new app with name NAME, I use app1 here.
 # app and be in an arbitary directory, better not be too far from main project
 # here I create all the apps under a directory "all_app", which is in the same directory of manage.py
 # therefore, I call the following command under the directory "all_app"
 python \path\to\manage.py startapp app1
 ```
   created tree structure
 ```
 app1/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
 ```
  now, add a new file ```urls.py``` under ```app1/```
 - urls.py
   - catch url of request from urls.py in main project
 - views.py
   - catch request from urls.py and return some response
 remember to add this app to main project after all set.
 ```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'all_app.app1.apps.PollsConfig',
]
```
 ## make a successful url request
 suppose we want to make a url request like ```localhost:8000/app1/hello_world/123```
1. add a new function, say ```hello_world```, in views.py of the app, say ```all_app\app1\views.py```
```python
from django.shortcuts import render
from django.http import HttpResponse
def index1(request, index):
 return HttpResponse("hello!!" + str(index))
```
2. add a new line in urls.py of main project, say ```tutorial_site\urls.py```
```python
from django.contrib import admin
from django.urls import path, include
# "include" means to cut the matching part and pass the rest to the included urls.py
# e.g. a request "localhost:8000/app1/hello_world/123" -> this file -> "hello_world/123" -> "app1\urls.py"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('all_app.app1.urls')),
]
```
3. add a new line in urls.py of app, say ```all_app\app1\urls.py```
```python
from django.contrib import admin
from django.urls import path, include
from . import views
# format <int:index> means it will convert the input to a int, and store it in a variable "index" 
# format <index> will directly store string
urlpatterns = [
    path('hello_world/<int:index>', views.hello_world),
]
```
4. finished!! go type ```python \path\to\manage.py runserver 8000``` and type ```localhost:8000/app1/hello_world/123``` in a browser!
## add model to sql
Now we want to add some class into sql table, how to do that?
Let's go to models.py in app, say ```all_app\app1\models.py```
add following lines into it
```python
from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField()
	def __str__(self):
		return self.question_text
	def some_function(self):
		return ('something')
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	number = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text
# ForeignKey means multiple Choice are mapped to one Question
# some frequently used operations
# Question.objects.all()
# Question.objects.filter(question_text__startwith='something'), where '__' represent some sort of '.'
# Question.objects.get(id=1)
# Question.objects.order_by('-pub_date'), '-pub_date' means sort in reverse order
# q = Question(question_text="some text", pub_date=timezone.now())
# q.choice_set, means all Choices that are mapped to Question, support count(), all(), etc.
# q.save(), save to db
# q.delete()
# q.choice_set.create(choice_text='something', number=10)
```
now we've add some model, then register it to app's admin.py, namely ```all_app\app1\admin.py``` to make admin be able to modify it
```python
from django.contrib import admin
from .models import Question, Choice
# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
```
then use ```makemigrations``` and ```migrate``` to make changes to db
```
# make changes according to the models.py we've just edited
# in this example, the \path\to\changed\app should be like all_app\app1
python \path\to\manage.py makemigrations \path\to\changed\app 
python \path\to\manage.py migrate
```
and we're done adding models!!
if you want to go further on this tutorial, don't forget to ```python \path\to\manage.py runserver``` and add some Choices in ```localhost:8000/admin``` or through ```python \path\to\manage.py shell```
## add template
now it's time to seperate html (template part) from views.py!!
first create a directory called ```templates``` under app's directory, namely ```all_app\app1\templates```
then create a directory named the same as the app (not forced, but easier for managing), namely ```all_app\app1\templates\app1```
then create our html file in it, and we can refer to it later by, say, ```app1.index.html```, credit to some setting in settings.py
let's create a ```index.html``` and add the following lines into it
```html
{% comment %}
{% some expression %}
{{ some variable }}
{% endcomment %}
{% if choice_list %}
	<ul>
	{% for choice in choice_list %}
		<li><a href="/app1/hello_world/{{ choice.number }}">{{ choice.choice_text }}</a></li>
	{% endfor %}
	</ul>
{% else %}
	<p>No questions are available.</p>
{% endif %}
```
then add a function in views.py to show this template, open views.py in your app, which should be ```all_app\app1\views.py``` here, and add following lines into it
```python
from django.shortcuts import render
from django.http import HttpResponse
from django import template
from .models import Question, Choice
def hello_world(request, index):
	return HttpResponse("hello!!" + str(index))

def index(request):
	t = template.loader.get_template('app1/index.html')
	choice_list = Choice.objects.all()
	return HttpResponse(t.render(locals(), request))
```
now we need to add a url to map to this function (index), so open urls.py in your app, which should be ```all_app\app1\urls.py``` here and add following lines into it
```
from django.contrib import admin
from django.urls import path, include
from . import views
# format <int:index> means it will convert the input to a int, and store it in a variable "index" 
# format <index> will directly store string
urlpatterns = [
    path('hello_world/<int:index>', views.hello_world),
    path('', views.index),
]
```
now run your web server and type ```localhost:8000/app1``` and have fun!!!
P.S. if you see nothing shown up after typing ```localhost:8000/app1``` in your web browser, you probably forgot to add some "Choice" to your database. To do this, either type ```localhost:8000/admin``` or use ```python \path\to\manage.py shell``` to add some.
## add form
To create forms in html file easily, we can rely on robust Django.
Create a file named forms.py under your app directory, which is ```all_app\app1\``` here.
```python
from django import forms

class FileForm(forms.Form):
	file_name = forms.CharField(label='file name', max_length = 100)
	file = forms.FileField()
```
now import ```FileForm``` in views.py and add a new function called upload
```python
from .forms import FileForm
def upload(request):
	if(request.POST):
		# create a form instance and populate it with data from the request:
		form = FileForm(request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			f = open('save_uploaded_file', 'wb')
			for chunk in request.FILES['file'].chunks():
				f.write(chunk)
			f.close()
			return HttpResponseRedirect('/app1')
	# if a GET (or any other method) we'll create a blank form
	else:
		form = FileForm()
	t = template.loader.get_template('app1/upload.html')
	return HttpResponse(t.render(locals(), request))
```
then add a template 
```html
<body>
	<form method="post" action='' enctype="multipart/form-data"> {% csrf_token %}
		{{ form.as_ul }}<br>
		<input type="submit" value="submit">
	</form>
</body>
```
all done!!
