from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path("login/", ObtainAuthToken.as_view()),
    path("accounts/", views.AccountView.as_view()),
    path("accounts/<pk>/", views.UpdateAccountView.as_view()),
    path("accounts/<pk>/management/", views.ActivateDeactivateAccountView.as_view()),
    path("accounts/newest/<int:num>", views.AccountView.as_view()),
]
