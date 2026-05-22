from django import forms
from .models import Category, Wallet, Transaction, Budget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên danh mục'}),
            'type': forms.Select(attrs={'class': 'form-input'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Icon'})
        }


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Tên ví:'}),
            'balance': forms.NumberInput(attrs={'placeholder': 'Số dư ban đầu'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Icon (vd: 💰 🏦 💳)'})
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'date', 'amount', 'transaction_type' ,'note', 'category', 'receipt']
        widgets = {
            'wallet': forms.Select(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Số tiền'}),
            'transaction_type': forms.Select(),
            'note': forms.Textarea(attrs={'placeholder': 'Ghi chú (Không bắt buộc)'}),
            'category': forms.Select(),
            'receipt': forms.FileInput(),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['wallet', 'amount', 'category', 'repeat' ,'start_date']
        widgets = {
            'wallet': forms.Select(),
            'amount': forms.NumberInput(attrs={'placeholder': 'Số tiền'}),
            'category': forms.Select(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'style': 'width:100%; padding:10px; border-radius:8px; border:1px solid #ccc; background:transparent; color:inherit;'}),
            'repeat': forms.Select(attrs={
                'style': 'width:100%; padding:10px; border-radius:8px; border:1px solid #ccc; background:var(--card-bg); color:inherit;'
            }),
        }