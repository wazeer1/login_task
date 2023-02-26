from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()
    username = serializers.CharField()
    phone = serializers.CharField()
    photo = serializers.ImageField(required=False,allow_null=True)
    email = serializers.CharField()


class LoginPassSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()