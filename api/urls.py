
from django.contrib import admin
from django.urls import path
from django.urls import include


from .views import PostView, PostCreateView #TestView

urlpatterns = [   
    #path('', TestView.as_view(), name='api_help_url'),
    #path('detail/<int:pk>', TestView.as_view()),
    path('posts/', PostView.as_view()),
    path('posts/create/', PostCreateView.as_view())
]
