from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from account.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
import json
import requests
from .models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # token = get_tokens_for_user(user)
    # Token.objects.create(user=user, access_token=token['access'])
    print('Registration Success >>>>>')
    return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Create or get an existing token for the user
            token = get_tokens_for_user(user)

            # Return the token key in the response
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            # Log the authentication failure
            print(f'Authentication failed for email: {email}')
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
      user = request.user
      print(user, 'request.user->')
      Token.objects.get(user=user).delete()
      # Log out the user and invalidate the token
      logout(request)

      return Response({'msg': 'Logout Successful'}, status=status.HTTP_200_OK)

def UserLogin(request):
  return render(request, 'account/login.html')


def UserRegister(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    name = request.POST.get('name')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    url = "http://127.0.0.1:8000/api/user/register/"

    payload = json.dumps({
      "email": email,
      "name": name,
      "password": password,
      "password2": password2
    })
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'csrftoken=ciIyQ0eD0MQQ4ipKfFnPyhIj8jDXirDn'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
  return render(request, 'account/register.html')



@api_view(['GET'])
def user_list(request, ):
    users = User.objects.all().order_by('name')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)