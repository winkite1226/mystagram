# user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in_view, name='sign-in'),
]