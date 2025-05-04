from django.urls import path
from . import views

urlpatterns = [
    path("test-auth/", views.TestAuthView.as_view(), name="test-auth"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh-token/", views.RefreshTokenView.as_view(), name="refresh-token"),
    path("", views.UserView.as_view(), name="user"),
]
