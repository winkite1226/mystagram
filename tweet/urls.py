# tweet/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tweet/', views.tweet, name='tweet'),
]