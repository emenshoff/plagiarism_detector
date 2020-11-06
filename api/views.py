from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
#security
from rest_framework.permissions import IsAuthenticated


from .serializers import PostSerializer
from .models import Post

API_PROTOCOL = 1.0

help_payload = {
        'protocol' : API_PROTOCOL,
        'lang' : "language, supported only 'ru'",
        'doc_format': "documement format, supported only 'txt' ",
        'content': 'document'
    }


# class TestView(APIView):

#     #permission_classes = (IsAuthenticated,)

#     def get(self, request, *args, **kwargs):
#         id = kwargs.get('pk')
#         print(f'id = {id}')
#         if id:
#             post = Post.objects.filter(pk__exact=id)
#             if id:
#                 serializer = PostSerializer(post[0], many=False)
#                 return Response(serializer.data)
#         else:
#             post_qs = Post.objects.all()
#             if post_qs:
#                 #post = post_qs.first()
#                 serializer = PostSerializer(post_qs, many=True)
#                 return Response(serializer.data)
#         return Response(help_payload)



#     def post(self, request, *args, **kwargs):
#         serializer = PostSerializer(data=request.data)
#         try:
#             serializer.is_valid()
#             serializer.save()
#             return Response(data=serializer.data)

#         except Exception as ex:
#             return Response(serializer.errors)



