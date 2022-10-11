# tweet/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('upload/', views.upload_post, name='upload'),
    path('profile/', views.profile, name='profile'),
]