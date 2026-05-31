from API.views import BudgetDetailAPIView
from API.views import TransactionDetailAPIView
from API.views import WalletDetailAPIView
from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    # Category API
    path('category/', CategoryAPIView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    # Wallet API
    path('wallet/', WalletAPIView.as_view(), name="wallet"),
    path('wallet/<int:pk>/', WalletDetailAPIView.as_view(), name="wallet_detail"),

    # Transaction API
    path('transaction/', TransactionAPIView.as_view(), name="transaction"),
    path('transaction/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction_detail'),

    # Budget API
    path('budget/', BudgetAPIView.as_view(), name="budget"),
    path('budget/<int:pk>/', BudgetDetailAPIView.as_view(), name="budget_detail"),    
]