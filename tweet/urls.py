# tweet/urls.py

from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('main/', views.main, name='main'),
    path('upload/', csrf_exempt(views.upload_post), name='upload'),
    path('profile/', views.profile, name='profile'),
]