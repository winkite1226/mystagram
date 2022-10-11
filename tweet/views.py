from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, Bookmark
from user.models import User
from uuid import uuid4
import os
from plamstagram.settings import MEDIA_ROOT
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def main(request):
    if request.method == 'GET':
        is_user = request.user.is_authenticated  # 사용자가 인증을 받았는지(로그인이 되어있는지)
        if is_user:
            user = request.user  # 로그인한 사용자 정보 불러오기
            print(user)
            print(user.user_id)
            all_tweet = Post.objects.all().order_by('-post_created_at')  # 저장된 모든 포스트 불러오기
            all_user = User.objects.all().exclude(user_nickname=user.user_nickname)  # 모든 유저
            post_list = []
            user_list = []
            print('hello')
            for person in all_user:
                user_list.append(dict(name=person.username, nickname=person.user_nickname, profile_image=person.user_profile_image))

            for tweet in all_tweet:  # tweet은 Post 인스턴스, 각 포스트에 대해
                user_post = User.objects.filter(user_id=tweet.post_author)  # 각 포스트를 작성한 사람
                all_comment = Comment.objects.filter(comment_postid=tweet.post_id)  # 한 포스터에 대한 모든 댓글들
                comment_list = []
                for comment in all_comment:  # 각 댓글에 대해
                    user_comment = User.objects.filter(user_id=comment.comment_author)  # 각 댓글을 작성한 사람
                    comment_list.append(dict(comment_content=comment.comment_content, nickname=user_comment.user_nickname))

                    #한개의 포스트 아이디에 is_like가 True인 것들의 개수를 센다  
                    like_count=Like.objects.filter(post_liked_postid=tweet.post_id, post_is_like=True).count()

                    #내가 이 게시글을 좋아요를 눌렀는지 안눌렀는지를 조회(exists 좋아요를 눌렀으면 True 안누르면 False로 반환)
                    #하트 불 들어오는지 안들어오는지 + like개수 카운트 기능
                    is_liked=Like.objects.filter(post_liked_postid=tweet.post_id, post_liked_userid=user, post_is_like=True).exists()
                    is_marked=Bookmark.objects.filter(post_bookmarkd_postid=tweet.post_id, post_bookmark_userid=user, post_is_marked=True).exists()
                    post_list.append(dict(id=tweet.post_id,
                                  image=tweet.post_image,
                                  content=tweet.post_content,
                                  like_count=like_count,
                                  profile_image=user_post.user_profile_image,
                                  nickname=user_post.user_nickname,
                                  reply_list=comment_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))
            return render(request, 'tweet/main.html', context=dict(feeds=post_list, user=user, people=user_list))

        else:
            return redirect('/user/sign-in/')

        
@api_view(['POST'])
@login_required
@csrf_protect
def upload_post(request):
    if request.method == 'POST':

        file = request.FILES['file']

        #랜덤으로 고유한 id값을 주기 위해서 uuid4사용(특수문자, 한글 섞여들어가면 오류가 날 수 있기 때문에)
        uuid_name = uuid4().hex 
        #/media/uuid랜덤이름 으로 저장되게 만든다
        print('ok')
        print(MEDIA_ROOT)
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        print('ok')
        print(MEDIA_ROOT)

        #실제로 저장하는 부분save_path에. 저장된 chunks에서 chuck를 하나하나 가져와서 사용한다.
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        image = uuid_name
        user = request.user  # 현재 로그인한 사용자를 불러오기

        my_post = Post()  # 게시글 모델 가져오기
        my_post.post_author = user.user_id  # 모델에 사용자 저장
        my_post.post_title = request.POST.get('input_feed_title', '')
        my_post.post_content = request.POST.get('input_feed_content', '')
        my_post.post_image = image
    
        my_post.save()
        print(file)
        print(image)
        return Response(status=200)


@login_required    
def profile(request):
    if request.method == 'GET':
        user = request.user  # 접속중인 사용자 불러오기
        if user is None:
            return render(request, 'user/signin.html')

        user = User.objects.filter(email=user.email).first()

        if user is None:
            return render(request, 'user/signin.html')

        feed_list = Post.objects.filter(post_author=user)
        like_list = list(Like.objects.filter(post_liked_userid=user, post_is_like=True).values_list('post_liked_postid', flat=True))
        like_feed_list = Post.objects.filter(post_id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(post_bookmark_author=user, post_is_marked=True).values_list('post_bookmarkd_postid', flat=True))
        bookmark_feed_list = Post.objects.filter(post_id__in=bookmark_list)

        return render(request, 'tweet/profile.html', context=dict(feed_list=feed_list, like_feed_list=like_feed_list, bookmark_feed_list=bookmark_feed_list, user=user))
