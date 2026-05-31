from rest_framework import serializers
from Finances.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'icon']
        read_only_fields = ['id']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'balance', 'icon']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'amount', 'transaction_type', 'category', 'note', 'date', 'receipt', 'created_at']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'wallet', 'category', 'amount', 'start_date', 'repeat']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)


