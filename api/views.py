from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser 
import json
from copy import deepcopy


# from rest_framework import generics
# #security
# from rest_framework.permissions import IsAuthenticated


from engine.shingles import ShingledTextCorpus
corpus = ShingledTextCorpus()


API_PROTOCOL = 1.0

api_info = {
        'version' : API_PROTOCOL,
        'language' : "language, supported only 'ru'",
        'doc_format': "documement format, supported only 'txt' ",
        'encoding': "utf-8",
        'content': 'document',  # документ в формате строки в запросе, список текстов, где найдены совпадения в ответе
        'result': '' # результат запроса.
    }

api_template = {
        'version' : API_PROTOCOL,
        'language' : "ru",
        'doc_format': "",
        'encoding': "utf-8",
        'content': "document",  
        'result': "" 
    }

def check_protocol(data):
    #  проверка корректности формата запроса
    refenence_fields = set(api_template.keys())
    data_fields = set(data.keys())
    if len(refenence_fields - data_fields):
        #print('wrong fields!')
        return False
    if any([
        (data['version'] != api_template['version']),
        (data['language'] != api_template['language']),
        (data['encoding'] != api_template['encoding'])
        ]):
        #print('wrong parameters!')

        return False
    return True
    

@api_view(['GET'])
def api_info(request, *args, **kwargs):
    return Response(api_info)


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def process_text(request, *args, **kwargs):  
    if request.method == 'POST':           
        if True:#check_protocol(data):
            data = dict(api_template)  
            #print(f'data = {request.POST}')

            text = deepcopy(request.POST.get('content'))   
            #print(f'text = {text}')         
            result = corpus.add_text(text)
            if result is None:
                data['result'] = 'Ok. Text succesfully added to the corpus!'
                data['content'] = ''  # не уверен, что корректно, но удалю (чтобы не гонять по сети порожняк)
            else:
                data['result'] = 'Plagiarism found! Similar sources are attached.'
                content = [text for text in result]
                data['content'] = content
            return Response(data)
    
    return Response(api_info)
    


