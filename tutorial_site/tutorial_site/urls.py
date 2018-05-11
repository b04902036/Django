from django.contrib import admin
from django.urls import path, include
# "include" means to cut the matching part and pass the rest to the included urls.py
# e.g. a request "localhost:8000/app1/hello_world/123" -> this file -> "hello_world/123" -> "app1\urls.py"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('app1/', include('all_app.app1.urls')),
]