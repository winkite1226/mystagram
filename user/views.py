from django.shortcuts import render
from django.contrib import auth  # 사용자 auth 기능

# Create your views here.
def sign_in_view(request):
    return render(request, 'user/signin.html')
