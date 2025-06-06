from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# IsAuthenticatedOrReadOnly는 인증된 사용자만 쓰기 작업을 수행할 수 있도록 허용하고,
# 인증되지 않은 사용자는 읽기 작업만 수행할 수 있도록 허용하는 권한 클래스입니다.
# IsAuthenticated는 
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permission

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    # APIView는 Django의 View와 유사하게 동작하는 클래스 기반 뷰입니다.
    # APIView는 HTTP 메서드에 따라 다른 동작을 수행할 수 있도록 메서드를 정의할 수 있습니다.
    # APIView는 Django REST Framework에서 제공하는 기본 클래스 중 하나로,
    # RESTful API를 구축할 때 유용하게 사용됩니다.

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
    
    def post(self, request):
        """Ceate a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'

            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST

            )
    
    ### put patch차이는 put은 성을 제공하면 성과 이름 전체 데이터가 성만으로 재설정되고
    ### patch는 성을 제공하면 성만 업데이트되는 함수이다.
    def put(self, request, pk=None):
        """Handle updating an object"""
        
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Delete and object"""

        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet""" 
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]


        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'

            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method':  'GET'})
    
    def update(self, equest, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # ModelViewSet은 Django REST Framework에서 제공하는 클래스 중 하나로,   
    # 모델에 대한 CRUD(Create, Read, Update, Delete) 작업을 자동으로 처리해주는 뷰셋입니다.
    # ModelViewSet은 Django의 모델과 연결되어 있으며, 모델의 데이터를 직렬화하고 역직렬화하는 기능을 제공합니다.
    # ModelViewSet은 기본적으로 list, create, retrieve, update, partial_update, destroy 등의 메서드를 제공합니다.
    authentiation_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewset(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permission.UpdateOwnStatus,
        IsAuthenticated
    )
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


