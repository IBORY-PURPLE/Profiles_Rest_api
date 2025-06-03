from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class HelloApiView(APIView):
    """Test API View"""

    # request는 클라이언트가 보내는 Http요청의 모든 정보를 담고 있는 객체
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as funtions (get, post, patch, put, delete)',
            'Is similar to traditional Django View',
            'Gives you thee most control over your Logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'HeLLo!', 'an_apiview': an_apiview})
    