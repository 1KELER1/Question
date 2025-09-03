from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from typing import List
from django.urls.resolvers import URLPattern

@api_view(['GET'])
def api_root(request, format=None):
    """
    Корневой endpoint API с ссылками на доступные ресурсы
    """
    return Response({
        'questions': reverse('qa_api:question-list-create', request=request, format=format),
        'admin': '/admin/',
        'docs': 'https://github.com/1KELER1/Question'
    })

urlpatterns: List[URLPattern] = [
    path('admin/', admin.site.urls),
    path('api/', include('qa_api.urls')),
]
