
from django.contrib import admin
from django.urls import path
from django.urls import include


from .views import PlagView

urlpatterns = [   
    #path('', TestView.as_view(), name='api_help_url'),
    #path('detail/<int:pk>', TestView.as_view()),
    path('', PlagView.as_view()),
]
