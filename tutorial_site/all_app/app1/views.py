from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from .models import Question, Choice
from .forms import FileForm
def hello_world(request, index):
	return HttpResponse("hello!!" + str(index))

def index(request):
	t = template.loader.get_template('app1/index.html')
	choice_list = Choice.objects.all()
	return HttpResponse(t.render(locals(), request))
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