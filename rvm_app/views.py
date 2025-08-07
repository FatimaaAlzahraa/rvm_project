from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import User, Deposit
from .serializers import (
    UserRegistrationSerializer, 
    LoginSerializer, 
    DepositSerializer, 
    UserSummarySerializer
)

#first user create your account (register)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user and return auth token"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        #your token in your account 
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login for the user have already account 
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return auth token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'total_points': user.total_points
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# the deposit your user (machineID , matrial type , and your matrial weight  )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_deposit(request):
    """Log a new recyclable deposit"""
    serializer = DepositSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        deposit = serializer.save()
        return Response({
            'message': 'Deposit logged successfully',
            'deposit': DepositSerializer(deposit).data,
            'new_total_points': request.user.total_points
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# your user all matrials added 
# your total deposits , total weight , how many deposits number , your fav matrial 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_summary(request):
    """Get user's recycling summary and stats"""
    serializer = UserSummarySerializer(request.user)
    return Response({
        'summary': serializer.data,
        'stats': {
            'total_deposits': request.user.deposits.count(),
            'avg_points_per_deposit': (
                request.user.total_points // max(request.user.deposits.count(), 1)
            ),
            'favorite_material': get_favorite_material(request.user)
        }
    })


def get_favorite_material(user):
    """Helper to find user's most recycled material type"""
    from django.db.models import Count
    result = (user.deposits
              .values('material_type')
              .annotate(count=Count('id'))
              .order_by('-count')
              .first())
    return result['material_type'] if result else None
