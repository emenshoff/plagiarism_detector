
from django.contrib import admin
from django.urls import path
from django.urls import include


from .views import api_info, process_text

urlpatterns = [   
    path('process/', process_text, name='api_process_url'),   
    path('', api_info, name='api_info_url'),
]
