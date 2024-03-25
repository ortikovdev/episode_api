from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2', 'created_date']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password2)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'last_login', 'modified_date', 'created_date']


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.ModelSerializer):
        password = serializers.CharField(min_length=6, max_length=64, write_only=True)
        password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)
        uidb64 = serializers.CharField(max_length=64, required=True)
        token = serializers.CharField(max_length=555, required=True)

        class Meta:
            model = User
            fields = ['password', 'password2', 'uidb64', 'token']

