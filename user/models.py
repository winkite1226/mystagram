from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table = 'user'

    user_id = models.AutoField(primary_key=True)  # 유저 모델의 아이디(기본키)
    user_email = models.EmailField(unique=True)  # 유저 이메일 주소
    user_nickname = models.CharField(max_length=24, unique=True)  # 유저의 닉네임
    user_phone = models.IntegerField()  # 유저 휴대폰번호
    user_name = models.CharField(max_length=24)  # 유저 실제 이름
    user_bio = models.TextField()  # 유저 자기소개
    user_profile_image = models.TextField()  # 유저 프로필 이미지
    
    USERNAME_FIELD: 'user_email'

