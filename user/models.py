from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table = 'user'

    user_id = models.AutoField(primary_key=True)  # 유저 모델의 아이디(기본키)
    email = models.EmailField('user email address', db_column='user_email', unique=True)  # 유저 이메일 주소
    user_nickname = models.CharField('user nickname', max_length=24, unique=True)  # 유저의 닉네임
    user_phone = models.IntegerField('user phone number', default=0)  # 유저 휴대폰번호
    username = models.CharField('user real name', db_column='user_name', max_length=24)  # 유저 실제 이름
    user_bio = models.TextField('user profile status message', default='')  # 유저 자기소개
    user_profile_image = models.TextField('user profile image', default='')  # 유저 프로필 이미지
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']