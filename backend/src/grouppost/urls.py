from django.urls import path
from .views import *

urlpatterns = [
    path('groups/allgroups/<str:uid>/',GroupView.as_view()),
    path('groups/post/<str:uid>/', PostView.as_view()),
    path('post/addlike/<int:uid>/', LikeView.as_view()),
    path('post/adddislike/<int:uid>/', Dislikeview.as_view()),
    path('post/comment/<int:uid>/',Comment.as_view()),
    path('post/group/bannuser/<int:uid>/',BannedUser.as_view())

]