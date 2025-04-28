from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='user'),
    path('test-auth/', views.TestAuthView.as_view(), name='test-auth'),
] 