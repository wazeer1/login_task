from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from api.v1.general.functions import generate_serializer_errors
from account.models import *
from django.contrib.auth.models import User
from main.encriptions import *
import requests
import json

@api_view(["POST"])
@permission_classes((AllowAny,))
def create_profile(request):
    serialized = SignUpSerializer(data = request.data)
    if serialized.is_valid():
        username = request.data["username"]
        password = request.data["password"]
        name = request.data["name"]
        email = request.data["email"]
        phone = request.data["phone"]
        try:
            photo = request.data["photo"]
        except:
            photo = None
        if not Profile.objects.filter(username = username).exists():
            if not Profile.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username = username,
                    password = password
                )
                profile = Profile.objects.create(
                    name = name,
                    username = username,
                    password = encrypt(password),
                    user = user,
                    email = email,
                    photo = photo,
                    phone = phone
                )
                response_data={
                    "StatusCode":6000,
                    "data":{
                        "title":"success",
                        "message":"succesfully created account"
                    }
                }
            else:
                response_data = {
                    "StatusCode":6001,
                    "data":{
                    "title":"failed",
                    "message":"account already exist with this number or email"
                    }
                }
        else:
            response_data = {
                "StatusCode":6001,
                "data":{
                    "title":"failed",
                    "message":"username already exists"
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            },
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login_pass(request):
    serialized = LoginPassSerializer(data = request.data)
    if serialized.is_valid():
        username = request.data["username"]
        password = request.data["password"]
        if Profile.objects.filter(username = username).exists():
            profile = Profile.objects.get(username=username)
            if password == decrypt(profile.password):
                headers = {
                    "Content-Type" : "application/json"
                }

                data = {
                    "username" : username,
                    "password" : password,
                }

                protocol = "http://"

                if request.is_secure():
                    protocol = "https://"
                host = request.get_host()
                url = protocol + host + "/api/v1/account/token/"
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    response_data={
                        "StatusCode":6000,
                        "data":{
                            "name":profile.name,
                            "response":response.json()
                        }
                    }
                else:
                    response_data={
                        "StatusCode":6001,
                        "data":{
                            "title":"failed",
                            "message":"something went wrong"
                        }
                    }
            else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"failed",
                        "message":"incorrect password"
                    }
                }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"failed",
                    "message":"no account with this username"
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            },
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def minimal(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    response_data={
        "StatusCode":6000,
        "data":{
        "name":profile.name
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)