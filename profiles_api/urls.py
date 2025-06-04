from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# DefaultRouter는 Django REST Framework에서 제공하는 라우터 클래스입니다.
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
]