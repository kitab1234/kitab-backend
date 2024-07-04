from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, CustomUser, Ibadat, Scale, IbadatItem
from .api.serializers import UserSerializer, CustomUserSerializer, IbadatSerializer, ScaleSerializer, IbadatItemSerializer
from datetime import date

###############################
#####     CUSTOM USER     #####
###############################

@api_view(['POST'])
def login(request):
    try:
        # Retrieve the user object based on username
        user = get_object_or_404(User, username=request.data['username'])

        # Check if the provided password matches the user's password
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid credentials"}, status=400)
      
        # Retrieve the custom user object associated with the user
        custom_user = get_object_or_404(CustomUser, user=user)

        # Generate or retrieve the token for the user
        token, _ = Token.objects.get_or_create(user=user)

        # Serialize user and custom_user data
        serializer = UserSerializer(user)
        serializer2 = CustomUserSerializer(custom_user)

        # Return response with token, user data, and custom user data
        return Response({
            'token': token.key,
            'user': serializer.data,
            'custom_user': serializer2.data
        })

    except Exception as e:
        # Handle exceptions and return a generic error response
        return Response({
            'error': str(e)
        }, status=500)
@api_view(['POST'])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the User instance
            user.set_password(request.data['password'])
            user.save()

            # Create Token for the user
            token = Token.objects.create(user=user)

            # Create CustomUserSerializer instance with data
            custom_user_data = {
                'user': user.id,
                'gender': request.data['gender'],  # Assuming gender is provided in request data
                'record_date': date.today()  # Use date.today() for current date
            }
            serializer2 = CustomUserSerializer(data=custom_user_data)
            if serializer2.is_valid():
                serializer2.save()
                return Response({
                    'token': token.key,
                    'user': serializer.data,
                    'custom_user': serializer2.data
                })

        return Response({
            'error': 'Invalid data for custom user creation',
            'serializer_errors': serializer2.errors if 'serializer2' in locals() else None,
            'user_serializer_errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        user = get_object_or_404(User, username=request.user.username)
        custom_user = get_object_or_404(CustomUser, user=user)
        
        # Update user first name
        user.first_name = request.data.get('first_name', user.first_name)
        
        # Update user password
        password = request.data.get('password')
        if password:
            user.set_password(password)
        
        # Save user object
        user.save()
        
        # Serialize user and custom user data
        serializer = UserSerializer(user)
        serializer2 = CustomUserSerializer(custom_user)
        
        return Response({ "user": serializer.data, "custom_user": serializer2.data })
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = get_object_or_404(User, username=request.user.username)
        user.delete()
        return Response({ "user deleted successfully" })
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
###############################
#######     IBADAT     ########
###############################

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ibadaat(request):
    try:
        # Retrieve authenticated user
        user = get_object_or_404(User, username=request.user.username)
        
        # Retrieve CustomUser instance associated with authenticated user
        custom_user = get_object_or_404(CustomUser, user=user)

        # Retrieve Ibadat instances associated with the custom_user
        ibadat_instances = Ibadat.objects.filter(user=custom_user)

        # Serialize the queryset
        serializer = IbadatSerializer(ibadat_instances, many=True)

        # Return serialized data as JSON response
        return Response({ "ibadat": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_ibadat(request):
    try:
        user = get_object_or_404(User, username=request.user.username)
        custom_user = get_object_or_404(CustomUser, user=user)
        data = { "name": request.data['name'].capitalize(), "user": custom_user.id }
        serializer = IbadatSerializer(data=data)
        if serializer.is_valid():
            # Save the serializer data to create a new Ibadat instance
            serializer.save()
            
            return Response({ "ibadat": serializer.data }, status=201)  # 201 Created
        return Response(serializer.errors, status=400)  # 400 Bad Request
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_ibadat(request, id):
    try:
        # Retrieve and update the specific Ibadat instance
        ibadat = get_object_or_404(Ibadat, id=id)
        
        # Update name if provided in request data
        if 'name' in request.data:
            ibadat.name = request.data['name'].capitalize()
        
        # Save the updated ibadat instance
        ibadat.save()
        
        # Serialize the updated ibadat instance
        ibadat_serializer = IbadatSerializer(ibadat)
        
        return Response({
            "ibadat": ibadat_serializer.data,
            "message": "Ibadat updated successfully"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_ibadat(request, id):
    try:
        # Retrieve and update the specific Ibadat instance
        ibadat = get_object_or_404(Ibadat, id=id)

        # Save the updated ibadat instance
        ibadat.delete()

        return Response({ "Ibadat deleted successfully" }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
###############################
########     SCALE     ########
###############################

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_scale(request, id):
    try:
        # Retrieve authenticated user
        user = get_object_or_404(User, username=request.user.username)
        
        # Retrieve CustomUser instance associated with authenticated user
        custom_user = get_object_or_404(CustomUser, user=user)
        ibadat = get_object_or_404(Ibadat, id=id, user=custom_user)
        # Retrieve Ibadat instances associated with the custom_user
        scale_instances = Scale.objects.filter(user=custom_user, ibadat=ibadat)

        # Serialize the queryset
        serializer = ScaleSerializer(scale_instances, many=True)

        # Return serialized data as JSON response
        return Response({ "scale": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_scale(request, id):
    try:
        user = get_object_or_404(User, username=request.user.username)
        custom_user = get_object_or_404(CustomUser, user=user)
        ibadat = get_object_or_404(Ibadat, id=id, user=custom_user)
        data = { "name": request.data['name'].capitalize(), "user": custom_user.id, "ibadat": ibadat.id, "color": request.data['color'] }
        serializer = ScaleSerializer(data=data)
        if serializer.is_valid():
            # Save the serializer data to create a new Ibadat instance
            serializer.save()
            
            return Response({ "scale": serializer.data }, status=201)  # 201 Created
        return Response(serializer.errors, status=400)  # 400 Bad Request
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_scale(request, id):
    try:
        scale = get_object_or_404(Scale, id=id)
        scale.name = request.data['name'].capitalize()
        scale.save()
        scale_serializer = ScaleSerializer(scale)
        return Response({
            "scale": scale_serializer.data,
            "message": "Ibadat updated successfully"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_scale(request, id):
    try:
        # Retrieve and update the specific Ibadat instance
        scale = get_object_or_404(Scale, id=id)

        # Save the updated ibadat instance
        scale.delete()

        return Response({ "Scale deleted successfully" }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
###############################
#####     IBADAT ITEM     #####
###############################

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ibadat_item(request, id):
    try:
        # Retrieve authenticated user
        user = get_object_or_404(User, username=request.user.username)
        
        # Retrieve CustomUser instance associated with authenticated user
        custom_user = get_object_or_404(CustomUser, user=user)
        ibadat = get_object_or_404(Ibadat, id=id, user=custom_user)
        # Retrieve Ibadat instances associated with the custom_user
        ibadat_item_instances = IbadatItem.objects.filter(user=custom_user, ibadat=ibadat)

        # Serialize the queryset
        serializer = ScaleSerializer(ibadat_item_instances, many=True)

        # Return serialized data as JSON response
        return Response({ "ibadat_item": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_ibadat_item(request, id):
    try:
        user = get_object_or_404(User, username=request.user.username)
        custom_user = get_object_or_404(CustomUser, user=user)
        ibadat = get_object_or_404(Ibadat, id=id, user=custom_user)
        data = { "name": request.data['name'].capitalize(), "user": custom_user.id, "ibadat": ibadat.id, "point": request.data['point'], "score": request.data['score'], "date": date.today() }
        serializer = IbadatItemSerializer(data=data)
        if serializer.is_valid():
            # Save the serializer data to create a new Ibadat instance
            serializer.save()
            
            return Response({ "ibadat_item": serializer.data }, status=201)  # 201 Created
        return Response(serializer.errors, status=400)  # 400 Bad Request
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_ibadat_item(request, id):
    try:
        ibadat_item = get_object_or_404(IbadatItem, id=id)
        ibadat_item.name = request.data['name'].capitalize()
        ibadat_item.point = request.data['point']
        ibadat_item.score = request.data['score']
        ibadat_item.save()
        ibadat_item_serializer = IbadatItemSerializer(ibadat_item)
        return Response({
            "ibadat_item": ibadat_item_serializer.data,
            "message": "Ibadat updated successfully"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_ibadat_item(request, id):
    try:
        # Retrieve and update the specific Ibadat instance
        ibadat_item = get_object_or_404(IbadatItem, id=id)

        # Save the updated ibadat instance
        ibadat_item.delete()

        return Response({ "Ibadat Item deleted successfully" }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)