from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomUserViewSet, IbadatViewSet, ScaleViewSet, IbadatItemSerializer

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet)
custom_user_router = DefaultRouter()
custom_user_router.register(r'custom_users', CustomUserViewSet)
ibadat_router = DefaultRouter()
ibadat_router.register(r'ibadat', IbadatViewSet)
scale_router = DefaultRouter()
scale_router.register(r'scale', ScaleViewSet)
ibadat_item_router = DefaultRouter()
ibadat_item_router.register(r'ibadat_item', ScaleViewSet)