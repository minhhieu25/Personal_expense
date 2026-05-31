from API.serializers import WalletSerializer
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Finances.models import *
from .serializers import *
# Create your views here.

# Category API View
class CategoryAPIView(APIView):
    def get(self, request):
        list_categories = Category.objects.filter(user=request.user)
        my_data = CategorySerializer(list_categories, many=True)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        my_data = CategorySerializer(data=request.data)
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        # cách cách viết tường minh
        # name = my_data.data['name']
        # type = my_data.data['type']
        # user = my_data.data['user']
        # icon = my_data.data['icon']
        # category = Category.objects.create(name=name, type=type, user_id=user, icon=icon)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_201_CREATED)

class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        my_data = CategorySerializer(category)
        return Response(my_data.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        my_data = CategorySerializer(category, data=request.data)
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        category.delete()
        return Response("Xoa thanh cong", status=status.HTTP_204_NO_CONTENT)

# Wallet API View
class WalletAPIView(APIView):
    def get(self, request):
        list_wallet = Wallet.objects.filter(user=request.user)
        my_data = WalletSerializer(list_wallet, many=True)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        my_data = WalletSerializer(data=request.data)
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_201_CREATED)

class WalletDetailAPIView(APIView):
    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        my_data = WalletSerializer(wallet)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        my_data = WalletSerializer(wallet, data=request.data)
        if not my_data.is_valid():
            return Response(my_data.data, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        wallet.delete()
        return Response("Xoa thanh cong" , status=status.HTTP_204_NO_CONTENT)


# TRansaction API View
class TransactionAPIView(APIView):
    def get(self, request):
        list_transaction = Transaction.objects.filter(user=request.user)
        my_data = TransactionSerializer(list_transaction, many=True, context={'request': request})
        return Response(my_data.data, status=status.HTTP_200_OK)

    def post(self, request):    
        my_data = TransactionSerializer(data=request.data, context={'request': request})
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_201_CREATED)


class TransactionDetailAPIView(APIView):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        my_data = TransactionSerializer(transaction, context={'request': request})
        return Response(my_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        my_data = TransactionSerializer(transaction, data=request.data, context={'request': request})
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        return Response("Xoa thanh cong", status=status.HTTP_204_NO_CONTENT)


#Budget API View
class BudgetAPIView(APIView):
    def get(self, request):
        list_budget = Budget.objects.filter(user=request.user)
        my_data = BudgetSerializer(list_budget, many=True, context={'request': request})
        return Response(my_data.data, status=status.HTTP_200_OK)

    def post(self, request):    
        my_data = BudgetSerializer(data=request.data, context={'request': request})
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_201_CREATED)

class BudgetDetailAPIView(APIView):
    def get(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        my_data = BudgetSerializer(budget, context={'request': request})
        return Response(my_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk): 
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        my_data = BudgetSerializer(budget, data=request.data, context={'request': request})
        if not my_data.is_valid():
            return Response(my_data.errors, status=status.HTTP_400_BAD_REQUEST)
        my_data.save(user=request.user)
        return Response(my_data.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        budget.delete()
        return Response("Xoa thanh cong", status=status.HTTP_204_NO_CONTENT)