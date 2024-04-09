import token

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, ResetPasswordSerializer, SetNewPasswordSerializer
from .tasks import send_mail_reset_passwd


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class MyProfileAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = User.objects.get(email=request.data['email']).email
        send_mail_reset_passwd.delay(email)
        return Response({"detail": "Reset link was sent to your email"})


class PasswordTokenCheckView(generics.GenericAPIView):
    # http://127.0.0.1:8000/user/v1/password-change-confirm/<uidb64>/<token/>
    serializer_class = ResetPasswordSerializer
    def get(self, request, uidb64, *args, **kwargs):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"success": False, "detail": "Invalid token, please try again"},
                                status=406)
            return Response({"success": True, "detail":"Successfully checked", 'uidb64': uidb64, 'token': token},
                            status=200)
        except DjangoUnicodeDecodeError as e:
            return Response({"success": False, "detail": f'Invalid token, please try again | {e.args}'},
                            status=401)


class SetPasswordView(generics.GenericAPIView):
    # http://127.0.0.1:8000/user/password-change-confirm/<uidb64>/<token/>
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"success": True, "message": "Password has been updated"}, status=200)
        return Response({"success": False, "message": "Credentials is invalid"}, status=406)
