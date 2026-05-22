from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category, Wallet, Transaction, Budget
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryForm, WalletForm, TransactionForm, BudgetForm
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
import calendar


# danh mục list
class CategoryView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        form = CategoryForm()  # Initialize empty form for GET request
        return render(request, "Finances/category/list.html", {
            'categories': categories,
            'form': form,
        })
    
    def post(self, request):
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            category = form.save(commit=False) # Chưa lưu vào db
            category.user = request.user # Gán user hiện tại
            category.save() # lưu vào db
            return redirect("finances:categories")
        
        #Form lỗi thì render lại group page và form
        categories = Category.objects.filter(user=request.user)
        return render(request, "Finances/category/list.html", {
            'categories': categories,
            'form': form,
        })
    
# sửa danh mục
class CategoryEditView(View): 
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        form = CategoryForm(instance=category)
        return render(request, "Finances/category/edit.html", {
            'form': form,
            'category': category,
        })

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('finances:categories')
        
# xóa dnah mục
class CategoryDeleteView(View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        category.delete()
        return redirect('finances:categories')

# list ví
class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user)

        # tính tổng số dư của tất cả các ví
        total = 0
        for i in wallet:
            total += i.balance
        # xử lý hiển thị dấu phẩy cho tổng số dư
        total_formatted = f"{total:,.0f} VNĐ"

        return render(request, "Finances/wallet/list.html", {
            'wallet': wallet,
            'total_formatted': total_formatted
        })

# thêm ví 
class WalletAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = WalletForm()
        return render(request, "Finances/wallet/add.html", {'form': form})

    def post(self, request):
        form = WalletForm(request.POST)

        if form.is_valid():
            wallet = form.save(commit=False) #chua luu vao db
            wallet.user = request.user #gan user hien tai
            wallet.save() # luu vao db
            return redirect("finances:wallet")
        
        # form loi thi render lai
        return render(request, "Finances/wallet/add.html", {'form': form})
    
# sửa ví
class WalletEditView(View):
    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        form = WalletForm(instance=wallet)
        return render(request, "Finances/wallet/edit.html", {
            'wallet': wallet,
            'form': form
        })
    
    def post(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('finances:wallet')
        
# xóa ví
class WalletDeleteView(View):
    def post(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
        wallet.delete()
        return redirect('finances:wallet')
    
# list giao dịch
class TransactionView(LoginRequiredMixin, View):
    def get(self, request):
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        transaction = Transaction.objects.filter(user=request.user)

        return render(request, "Finances/transaction/list.html", {
            'form': form,
            'transaction': transaction,
        })
    
    def post(self, request):
        form =  TransactionForm(request.POST, request.FILES)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False) # chua luu vao db
            transaction.user = request.user # gan user hien tai
            transaction.save() # luu vao db
            return redirect("finances:transaction")
        return render(request, "Finances/transaction/list.html", {'form': form})

# sửa giao dịch
class TransactionEditView(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        form = TransactionForm(instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        return render(request, "Finances/transaction/edit.html", {
            'transaction': transaction,
            'form': form
        })
    
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            return redirect("finances:transaction")
        
# xóa giao dịch
class TransactionDeleteView(View):
    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        return redirect("finances:transaction")

# list ngân sách
class BudgetView(LoginRequiredMixin, View):
    def get(self, request):
        budget = Budget.objects.filter(user=request.user)
        repeat_filter = request.GET.get('repeat', 'all')
        
        # Lọc theo repeat nếu không phải 'all'
        if repeat_filter != 'all':
            budget = budget.filter(repeat=repeat_filter)
        
        summary = Budget.total_summary(request.user)
        return render(request, "Finances/budget/list.html", {
            'budget': budget,
            'summary': summary,
            'repeat_filter': repeat_filter,
        })

# thêm ngân sách
class BudgetAddView(LoginRequiredMixin, View): 
    def get(self, request):
        form = BudgetForm()
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(user=request.user, type="Chi tiêu")
        return render(request, "Finances/budget/add.html", {'form': form})

    def post(self, request):
        form = BudgetForm(request.POST)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(user=request.user, type="Chi tiêu")
        if form.is_valid():
            budget = form.save(commit=False) # chua cho luu
            budget.user = request.user # gan user hien tai
            budget.save() # luu vao db
            return redirect("finances:budget")
        return render(request, "Finances/budget/budget_add.html", {'form': form })

# sửa ngân sách 
class BudgetEditView(View):
    def get(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        form = BudgetForm(instance=budget)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(user=request.user, type='Chi tiêu')
        return render(request, "Finances/budget/edit.html", {
            'budget': budget,
            'form': form
        })

    def post(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        form = BudgetForm(request.POST, instance=budget)
        form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(user=request.user, type='Chi tiêu')
        if form.is_valid():
            form.save()
            return redirect("finances:budget")
        
# xóa ngân sách
class BudgetDeleteView(View):
    def post(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk, user=request.user)
        budget.delete()
        return redirect("finances:budget")

# lịch
class CalenderView(View):
    def get(self, request):
        # lấy filter từ url
        view_type = request.GET.get('view', 'month')
        date_str = request.GET.get('date', None)

        # ngày được chọn là hôm nay
        if date_str:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            selected_date = timezone.now().date()

        # tạo lịch tháng
        cal = calendar.monthcalendar(selected_date.year, selected_date.month)

        # lấy tất cả transaction trong tháng
        transactions = Transaction.objects.filter(
            user=request.user,
            date__month = selected_date.month,
            date__year = selected_date.year
        )

        # group transaction theo ngay hien thi tren lich
        transaction_by_date = {}
        for t in transactions:
            day = t.date.day
            if day not in transaction_by_date:
                transaction_by_date[day] = {'income': 0, 'expense': 0}
            if t.transaction_type == 'Thu nhập':
                transaction_by_date[day]['income'] += t.amount
            else:
                transaction_by_date[day]['expense'] += t.amount

        # tháng trước/sau để điều hướng
        if selected_date.month == 1:
            prev_month = selected_date.replace(year=selected_date.year - 1, month=12, day=1).strftime('%Y-%m-%d')
        else:
            prev_month = selected_date.replace(month=selected_date.month -1, day=1).strftime('%Y-%m-%d')

        if selected_date.month == 12:
            next_month = selected_date.replace(year=selected_date.year + 1, month=1, day=1).strftime('%Y-%m-%d')
        else:
            next_month = selected_date.replace(month=selected_date.month + 1, day=1).strftime('%Y-%m-%d')

        # Tổng thu chi
        total_income = transactions.filter(transaction_type='Thu nhập').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='Chi tiêu').aggregate(Sum('amount'))['amount__sum'] or 0
        total_difference = total_income - total_expense
        

        # Ngày được chọn trên lịch
        selected_day = request.GET.get('selected_day', None)
        if selected_day:
            selected_day = int(selected_day)

        # lấy giao dịch của ngày được chọn
        day_transactions = None
        if selected_day:
            day_transactions = Transaction.objects.filter(
                user=request.user,
                date__day=selected_day,
                date__month=selected_date.month,
                date__year=selected_date.year,
            )
        
        return render(request, "Finances/calendar/calendar.html", {
                'cal': cal,
                'selected_date': selected_date,
                'transaction_by_date': transaction_by_date,
                'total_income': total_income,
                'total_expense': total_expense,
                'total_difference': total_difference,
                'prev_month': prev_month,
                'next_month': next_month,
                'month_name': selected_date.strftime('%B %Y'),
                'selected_day': selected_day,
                'day_transactions': day_transactions,
        })


# setting
class SettingView(View):
    def get(self, request):
        return render(request, "Finances/settings.html")
    
    
# bao cao
class ReportView(View):
    def get(self, request):
        return render(request, "Finances/report.html")
