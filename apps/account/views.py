from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, ResetPasswordSerializer
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
        user = User.objects.get(email=request.data['email'])
        send_mail_reset_passwd(user)
        return Response({"detail": "Reset link was sent to your email"})