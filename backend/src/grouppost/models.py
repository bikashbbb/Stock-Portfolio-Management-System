from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField

# Create your models here.
class Groups(models.Model):
    groupname = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE,related_name='group_created_by')

    def __str__(self) -> str:
        return self.groupname

class AllPosts(models.Model):
    groupid = models.ForeignKey(Groups,on_delete=models.CASCADE, related_name='groupid',null=True)
    post_title = models.TextField(null=False)
    post_likes_count = models.IntegerField(null=True)
    post_description = models.TextField(null=False)
    post_author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_author')
    post_likes = models.ManyToManyField(User,blank=True, related_name= 'likes',default=None)
    post_dislikes = models.ManyToManyField(User,blank=True, related_name='dislikes',default=None)
    post_comments = models.ManyToManyField(User,blank=True, related_name='comments',default=None)

class Comments(models.Model):
    comment_title = models.TextField(null=False)
    comment_author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_comment')
    post_id = models.ForeignKey(AllPosts,on_delete=models.CASCADE,related_name='postid')