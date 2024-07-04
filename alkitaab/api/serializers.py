from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from ..models import CustomUser, Ibadat, Scale, IbadatItem

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'password', 'date_joined']
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user', 'gender', 'record_date']
class IbadatSerializer(ModelSerializer):
    class Meta:
        model = Ibadat
        fields = ['id', 'user', 'name']
class ScaleSerializer(ModelSerializer):
    class Meta:
        model = Scale
        fields = ['id', 'user', 'ibadat', 'name', 'color']
class IbadatItemSerializer(ModelSerializer):
    class Meta:
        model = IbadatItem
        fields = ['id', 'user', 'ibadat', 'name', 'point', 'score', 'date']