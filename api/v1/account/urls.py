from django.urls import path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from . import views


app_name = "api_v1_accounts"

urlpatterns = [
    #simplejwt urls
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #profile apis
    re_path(r'^signup-user/$', views.create_profile, name="signup_user"),
    re_path(r'^login-password/$', views.login_pass, name="login_user"),
    re_path(r'^minimal/$', views.minimal, name="minimal"),


]