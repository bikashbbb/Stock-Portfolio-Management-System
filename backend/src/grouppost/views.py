from logging import exception
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view

class GroupView(APIView):
    @swagger_auto_schema(operation_description="uid can be none", responses={404: 'slug not found',
    200:"all group serialized data"
    })
    def get(self,request,uid=None):
        groups_object = Groups.objects.all()
        serializedd = GroupSerializer(groups_object,many=True)
        return Response(serializedd.data)

    @swagger_auto_schema(
        operation_description="uid: Username ",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'groupname': openapi.Schema(type=openapi.TYPE_STRING, description='name of group to create'),
        }),responses={200:'Group created sucessfully',404:"only admins/staffs can create groups"})
    def post(self,request,uid,format=None):
        # TODO: if uid is admin == true then only create group
        Userid = User.objects.get(username = uid)
        if Userid.is_staff == True:
            Groups.objects.create(groupname= request.data['groupname'],created_by =Userid )
            return Response(data={
                'Group created sucessfully'
            })
        else:
            return Response(data={
                'only admins/staffs can create groups'
            })
    @swagger_auto_schema(operation_description="uid: groupname_username", responses={404: 'Group doesnt exist',
    200:"Group deleted sucessfully"
    })
    def delete(self,request,uid):
        username = uid.split('_')
        if User.objects.get(username = username[1]).is_staff == True:
            try:
                groupobj = Groups.objects.get(groupname = username[0])
                groupobj.delete()
                return Response(data={
                        'Group deleted sucessfully'
                    })
            except exception:
                return Response(data={
                    'Group doesnt exist '
                })
        else:
            return Response(data={
                    'only user can delete group '
                })


class PostView(APIView):
    @swagger_auto_schema(operation_description="uid: id of the group to get the post from", responses={404: 'No post available',
    200:"all Post serialized data"
    })
    def get(self,request,uid=None):
      
        groupobj = Groups.objects.get(id=uid)
        all_post_objects = AllPosts.objects.filter(groupid= groupobj)
        serialize = PostSerializer(all_post_objects,many=True)
        return Response(serialize.data)

    @swagger_auto_schema(
        operation_description="uid: id of the group to post at",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'post_title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the post'),
            'post_author': openapi.Schema(type=openapi.TYPE_STRING, description='username of writer of the post'),
            'post_description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the post'),

        }),responses={200:'Group created sucessfully',404:"only admins/staffs can create groups"})
    def post(self,request,uid):       
        obj = Groups.objects.get(id=uid)
        postauthor = User.objects.get(username = request.data['post_author'])
        AllPosts.objects.create(post_title=request.data['post_title'],
        post_likes_count= 0,
            post_description= request.data['post_description'],
            groupid = obj,
            post_author = postauthor,
            )
        return Response({"post created sucessfully"})

    @swagger_auto_schema(operation_description="uid: id of the post", responses={404: 'No post available',
    200:"Post deleted sucessfully"
    })   
    def delete(self,request,uid):
        #AllPosts.objects.get(post_author= )
        todelet = AllPosts.objects.get(id=uid)
        if todelet.exists():
            todelet.delete()
            return Response({
                "Post deleted sucessfully"
            })

class LikeView(APIView):
    @swagger_auto_schema(operation_description="uid: id of the post , see if the user has liked the post with the post id", responses={404: 'No post available',
    200:"all Post serialized data"
    })
    
    def get(self,request,uid,):
        # get if user has liked in the current post
        if request.user.is_authenticated:
            current_post = AllPosts.objects.get(id=uid)
            for likes in current_post.post_likes.all():
                if likes == request.user:
                    return Response({'True'})
                else:
                    return Response({'False'})
            return Response({'User hasnot liked '})
        else:
            return Response({'User must login'})

    @swagger_auto_schema(operation_description="uid: id of the post , when clicked on like", responses={404: 'No post available',
    200:"all Post serialized data"
    })
    def post(self,request,uid):
        # when user clicks on like

        current_post = AllPosts.objects.get(id=uid) 
        if request.user.is_authenticated:

            for dislikes in current_post.post_dislikes.all():
                if dislikes == request.user:
                    current_post.post_dislikes.remove(request.user)
                    current_post.save()

            for likes in current_post.post_likes.all():
                if likes == request.user:
                    current_post.post_likes.remove(request.user)
                    current_post.post_likes_count -=1         
                else:
                    current_post.post_likes.add(request.user)
                    current_post.post_likes_count +=1
            current_post.save()
            return Response(PostSerializer(current_post).data)
        else:
            return Response("User must loggin")

class Dislikeview(APIView):
    @swagger_auto_schema(operation_description="uid: id of the post ,check user has disliked this post", responses={404: 'No post available',
    200:"all Post serialized data"
    })
    def get(self,request,uid):
        # get if the user has disliked the post
        current_post = AllPosts.objects.get(id=uid)
        for dislikes in current_post.post_dislikes.all():
            if dislikes == request.user:
                return Response({'True'})
            else:
                return Response({'False'}) 
    @swagger_auto_schema(operation_description="uid: id of the post , when clicked on dislike", responses={404: 'No post available',
    200:"all Post serialized data"
    })
    def post(self,request,uid):
        current_post = AllPosts.objects.get(id=uid) 
        if request.user.is_authenticated:
            for likes in current_post.post_likes.all():
                if likes == request.user:
                    current_post.post_likes.remove(request.user)
                    current_post.save()
                    
            for dilikes in current_post.post_dislikes.all():
                if dilikes == request.user:
                    current_post.post_dislikes.remove(request.user)
                    current_post.post_dislikes_count -=1         
                else:
                    current_post.post_dislikes.add(request.user)
                    current_post.post_dislikes_count +=1
            current_post.save()
            return Response(PostSerializer(current_post).data)
        else:
            return Response('User must login')
        

class Comment(APIView):
    @swagger_auto_schema(operation_description="uid: id of the post", responses={404: 'No comments available',
    200:"all Post serialized data"
    })
    def get(self,request,uid):
        # check if the comments of a post
        if request.user.is_authenticated:
            all_comments = Comments.objects.filter(post_id= uid)
            return Response(CommentSerializer(all_comments))      
        else:
            Response('user must login')  

    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'comment_title': openapi.Schema(type=openapi.TYPE_STRING, description='comment'),
            'comment_author': openapi.Schema(type=openapi.TYPE_STRING, description='username of writer of the comment'),
            'post_id': openapi.Schema(type=openapi.TYPE_STRING, description='id of the post'),

        }),responses={200:'Group created sucessfully',404:"only admins/staffs can create groups"})  
    def post(self,request,uid):
        # todo make it from request.user 
        author = User.objects.get(username = request.body['username'])
        Comments.objects.create(
           comment_title= request.body['comment_title'],
           comment_author = author,
           post_id = AllPosts.objects.get(id=uid)
        )
    @swagger_auto_schema(operation_description="uid: id of the comment", responses={404: 'No comments available',
    200:"Comment deleted sucessfully"
    })
    def delete(self,request,uid):
        if request.user.is_authentiated:
            delete_obj = Comments.objects.get(id=uid)
            if delete_obj.author == request.user:
                delete_obj.delete()
                return Response(
                    'Comment deleted sucessfully'
                )
            else:
                return Response('Comment id invalid')
        else:
            return Response('User must login')


class BannedUser(APIView):
    @swagger_auto_schema(            
            request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'groupid': openapi.Schema(type=openapi.TYPE_STRING, description='name of group to bann user'),
        })
        )   
        
    def post(self,request,uid):
        try:
            userobj = User.objects.get(id=uid)
            obj=  Group.objects.get(id=request.body['groupid'],
                )
            obj.bannedusers.add(userobj)
            return Response({'messege':'User banned sucess'},
            status=200
            )
        except Exception:
            return Response({'messege':'invalid body'},
            status=200
            )


class IsUserBanned(APIView):

    @swagger_auto_schema( 
        operation_description='uid: username of the user',           
            request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'groupid:': openapi.Schema(type=openapi.TYPE_STRING, description='1'),
            
        })
        )     
    def post(self,request,uid):
        obj = Groups.objects.get(id=request.body['groupid'])
        user = User.objects.get(username=uid)
        if user in obj.bannedusers:
            return Response(
                
                {"messege":True},
                status=200
            )
        else:
            return Response(
            
            {
                "messege":False
            },status=401)






