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