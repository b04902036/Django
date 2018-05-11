from django.contrib import admin
from django.urls import path, include
from . import views
# format <int:index> means it will convert the input to a int, and store it in a variable "index" 
# format <index> will directly store string
urlpatterns = [
    path('hello_world/<int:index>', views.hello_world),
    path('', views.index),
]