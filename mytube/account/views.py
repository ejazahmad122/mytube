from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login
from account.serializers import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.serializers import UserProfileSerialier
from account.serializers import UserChangePasswordVSerializer
from account.serializers import SendPasswordResetEmailSerializer
from account.serializers import UserResetPasswordSerializer
from account.utils import get_tokens_for_user


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        """create the user in realated models model:User

        Args:
            request (http): hold the request data 

        Returns:
            response(json): registered user data
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': "User Registered successfully !!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        """authorize the user and logged in

        Args:
            request (http): hold the request data 

        Returns:
            response(json): JWT token
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': "Login successfully !!"}, status=status.HTTP_202_ACCEPTED)
            return Response({'errors': "email or password invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'errors': {'nonfield_errors': [serializer.errors]}}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """give the data about current logged in user

        Args:
            request (http): hold the request data

        Returns:
           response(json): status about the request with user data
        """
        serializer = UserProfileSerialier(request.user)
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """take the new password and change in related model model:User

        Args:
            request (http): hold the request data 

        Returns:
            response(json): status about the request
        """
        serializer = UserChangePasswordVSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Change successfully !!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        """send the email to the user with reset password email

        Args:
            request (http): hold the request data 

        Returns:
            response(json): status about the request
        """
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Reset Email has been send successfully !!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    def post(self, request, uid, token, format=None):
        """set the new password with emailed token authorization

        Args:
            request (http): hold the request data
            uid (int): user id
            token (jwt): emailed token

        Returns:
           response(json): status about the request
        """
        serializer = UserResetPasswordSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password Reset successfully !!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
