from django.shortcuts import render, redirect
from django.contrib import auth  # 사용자 auth 기능
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model  # 사용자가 있는지 검사하는 함수

# Create your views here.
def sign_in_view(request):

    if request.method == 'GET':
        return render(request, 'user/signin.html')
    
    elif request.method == 'POST':
        useremail = request.POST.get('input_email', None)
        userpassword = request.POST.get('input_password', None)

        # 사용자 불러오기
        me = auth.authenticate(request, email=useremail, password=userpassword)
        # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:  # 로그인 실패 시
            return redirect('/sign-in')


# 회원가입
def sign_up_view(request):

    if request.method == 'GET':
        return render(request, 'user/signup.html')

    elif request.method == 'POST':
        useremail = request.POST.get('input_email', None)
        username = request.POST.get('input_name', None)
        usernickname = request.POST.get('input_nickname', None)
        userpassword = request.POST.get('input_password', None)
        userpassword2 = request.POST.get('input_password2', None)

        # 비밀번호가 일치하지 않은 경우
        if userpassword != userpassword2:
            msg = '비밀번호가 일치하지 않습니다.'
            return render(request, 'user/signup.html', {'message': msg})
        else:
            exist_user = get_user_model().objects.filter(email=useremail)

            # 사용자가 존재하는 경우
            # 사용자를 저장하지 않고, 회원가입 페이지를 다시 띄움
            if exist_user:
                msg = '이미 존재하는 이메일입니다.'
                return render(request, 'user/signup.html', {'message': msg})
            else:
                User.objects.create_user(username=username, email = useremail, password=userpassword, user_nickname=usernickname)
                return redirect('/sign-in')  # 회원가입 완료 후 로그인 페이지로 이동
