from django.db import models

# Create your models here.
# 게시글 모델
class Post(models.Model):
    class Meta:
        db_table = 'post'

    post_id = models.AutoField(primary_key=True)  # 게시글 아이디
    post_author = models.ForeignKey('user.User', related_name='post', on_delete=models.CASCADE, db_column='post_author')  # 게시글 작성자
    post_title = models.CharField(max_length=24)  # 게시글 제목
    post_content = models.TextField()  # 게시글 내용
    post_created_at = models.DateTimeField(auto_now_add=True)  # 게시글 작성일
    post_updated_at = models.DateTimeField(auto_now=True)  # 게시글 수정일
    post_image = models.TextField()  # 게시글 이미지


# 댓글 모델
class Comment(models.Model):
    class Meta:
        db_table = 'comment'

    comment_id = models.AutoField(primary_key=True)  # 댓글 아이디
    comment_postid = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE, db_column='comment_postid')  # 댓글단 포스트 번호
    comment_author = models.ForeignKey('user.User', related_name='comment', on_delete=models.CASCADE, db_column='comment_author')  # 댓글 작성자 이메일
    comment_content = models.TextField()  # 댓글 내용
    comment_created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성일
    comment_updated_at = models.DateTimeField(auto_now=True)  # 댓글


# 게시글 좋아요 모델
class Like(models.Model):
    class Meta:
        db_table = 'like'

    post_liked_id = models.AutoField(primary_key=True)  # 게시글 좋아요 아이디
    post_liked_postid = models.ForeignKey(Post, related_name='like', on_delete=models.CASCADE, db_column='post_like_postid')  # 좋아요한 포스트번호
    post_liked_userid = models.ForeignKey('user.User', related_name='like', on_delete=models.CASCADE, db_column='post_like_userid')  # 좋아요한 작성자 이메일
    post_is_like = models.BooleanField(default=True)  # 좋아요 여부 -> 해제를 위해


# 게시글 북마크 모델
class Bookmark(models.Model):
    class Meta:
        db_table = 'bookmark'

    post_bookmared_id = models.AutoField(primary_key=True)  # 게시글 북마크 아이디
    post_bookmarkd_postid = models.ForeignKey(Post, related_name='bookmark', on_delete=models.CASCADE, db_column='bookmark_postid')  # 북마크한 포스트 번호
    post_bookmark_author = models.ForeignKey('user.User', related_name='bookmark', on_delete=models.CASCADE, db_column='bookmark_author')  # 북마크한 작성자 이메일 주소
    post_is_marked = models.BooleanField(default=True)  # 북마크 여부 -> 해제를 위한