from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from ..models import CustomUser, Ibadat, Scale, IbadatItem
from .serializers import UserSerializer, CustomUserSerializer, IbadatSerializer, ScaleSerializer, IbadatItemSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
class IbadatViewSet(ModelViewSet):
    queryset = Ibadat.objects.all()
    serializer_class = IbadatSerializer
class ScaleViewSet(ModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer
class ScaleViewSet(ModelViewSet):
    queryset = IbadatItem.objects.all()
    serializer_class = IbadatItemSerializer