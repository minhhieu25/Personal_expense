from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.AuthView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
