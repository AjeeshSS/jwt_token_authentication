from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.db.models import Q
import os

from .serializers import RegistrationUserSerializer, UserSerializer


class RegisterUser(APIView):
    """view for registering new user."""

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = RegistrationUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)

            user = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistRefreshView(APIView):
    """Pass refresh token to Blacklist"""
    
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
      
"""The BlacklistTokenUpdateView is used to handle the revocation of refresh tokens. When a user logs out or their 
access token expires, the refresh token can be used to obtain a new access token without requiring the user to 
login again. However, if a user's refresh token is stolen or compromised, an attacker could use it to obtain new access
tokens even after the user has logged out or changed their password. To prevent this, refresh tokens can be blacklisted 
or revoked, so that they can no longer be used to obtain new access tokens."""
            
class UserListView(APIView):
    """view for user list."""
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class GetUser(APIView):
    """retrieve a user with an id."""
    # permission_classes = [IsAuthenticated]
    
    def get(self,request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)        
        except User.DoesNotExist:
            raise Http404


class EditUser(APIView):
    """edit an user details."""

    def post(self, request ,id):
        user = User.objects.get(id=id)
        userData =  UserSerializer(instance=user, data=request.data, partial=True)
        if userData.is_valid():
            userData.save()
            return Response(userData.data, status=status.HTTP_200_OK)
        return Response(400)


class DeleteUser(APIView):
    """view for deleting a user."""
    
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            profile_picture_path = user.profile_picture.path
            user.delete()
            if os.path.exists(profile_picture_path):
                os.remove(profile_picture_path)
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response("Customer does not exist.")


class SearchUserView(APIView):
    """view for searching an user."""
    
    def get(self, request):
        name = request.GET.get('name')
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        users = User.objects.filter(name=user.name)
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)
    