from django.contrib.auth import models
from rest_framework.serializers import ModelSerializer
from .models import AllPosts,Comments,Groups

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'
        depth = 1

class PostSerializer(ModelSerializer):
    class Meta:
        model = AllPosts
        fields = '__all__'
        

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        depth = 1


        