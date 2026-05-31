from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.AuthView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    # customuser
    path('customuser/', views.CustomUserView.as_view(), name="customuser"),
    path('customuser/edit/', views.CustomUserEditView.as_view(), name="edit_user"),
    path('password_change/', views.PasswordChangeView.as_view(), name="password_change"),
]
