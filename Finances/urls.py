from django.urls import path
from .views import *

app_name = 'finances'
urlpatterns = [
    # giao dich (tạm để là index, sau này sửa lại thành transaction)
    path('transaction/', TransactionView.as_view(), name="transaction"),
    path('transaction/<int:pk>/edit/', TransactionEditView.as_view(), name="transaction_edit"),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name="transaction_delete"),

    # danh muc
    path('categories/', CategoryView.as_view(), name="categories"),
    path('categories/<int:pk>/edit/', CategoryEditView.as_view(), name="category_edit"),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name="category_delete"),

    # vi
    path('wallet/', WalletView.as_view(), name="wallet"),
    path('wallet/add/', WalletAddView.as_view(), name="wallet_add"),
    path('wallet/<int:pk>/edit/', WalletEditView.as_view(), name="wallet_edit"),
    path('wallet/<int:pk>/delete/', WalletDeleteView.as_view(), name="wallet_delete"),

    # ngân sách
    path('budget/', BudgetView.as_view(), name="budget"),
    path('budget/add/', BudgetAddView.as_view(), name="budget_add"),
    path('budget/<int:pk>/edit/', BudgetEditView.as_view(), name="budget_edit"),
    path('budget/<int:pk>/delete/', BudgetDeleteView.as_view(), name="budget_delete"),
    
    # lịch
    path('calendar/', CalenderView.as_view(), name="calendar"),

    # # setting
    # path('settings/', SettingView.as_view(), name="settings"),

    # bao cao
    path('report/', ReportView.as_view(), name="report"),

]