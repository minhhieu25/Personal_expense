from django.db import models
from django.utils import timezone
from django.db.models import Sum
import calendar

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('Thu nhập', 'Thu nhập'), ('Chi tiêu', 'Chi tiêu')])
    user = models.ForeignKey('Users.CustomUser' ,on_delete=models.CASCADE, related_name='categories')
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        # ràng buộc trong bảng Category không đc tồn tại 2 bản ghi có cùng name, user, type
        unique_together = ('name', 'user', 'type')
        # trong admin hiện thị Categories (tránh trường hợp admin tự thêm s: Categorys)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Wallet(models.Model):
    user = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        # ràng buộc trong bảng Wallet không được xuất hiện 2 bản ghi có cùng name
        unique_together = [('name')]
        verbose_name_plural = 'Wallets'

    def balance_vnd(self):
        return f"Số dư: {self.balance:,.0f} đ"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    user = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE, related_name='transactions')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('Thu nhập', 'Thu'), ('Chi tiêu', 'Chi')])
    # PROTECT: bảo vệ dữ liệu con(Transaction) khỏi việc mất liên kết khi xóa dự liệu cha(Category)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    note = models.CharField(blank=True)
    date = models.DateField(default=timezone.now)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''-date: sx theo trường date giảm dần
           -created_at: nếu nhiều bản ghi có cùng date thì sx theo created_at giảm dần
        '''
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.amount:,}đ - {self.category.name} ({self.get_transaction_type_display()})"

    def amount_vnd(self):
        return f"{self.amount:,.0f}"

    def save(self, *args, **kwargs):
        if self.pk:  # Sửa giao dịch
            old = Transaction.objects.get(pk=self.pk)
            
            # Kiểm tra ví có thay đổi không (so sánh ID, không phải object)
            wallet_changed = old.wallet.id != self.wallet.id
            
            if wallet_changed:
                # Nếu ví thay đổi: hoàn lại ví cũ, cộng ví mới
                if old.transaction_type == "Thu nhập":
                    old.wallet.balance -= old.amount
                else:
                    old.wallet.balance += old.amount
                old.wallet.save()
                
                # Cộng vào ví mới
                if self.transaction_type == "Thu nhập":
                    self.wallet.balance += self.amount
                else:
                    self.wallet.balance -= self.amount
                self.wallet.save()
            else:
                # Ví không thay đổi: cơ sở dữ liệu vẫn là balance cũ
                # Phải hoàn lại tiền cũ trước, rồi cộng tiền mới
                
                # Hoàn lại giao dịch cũ
                if old.transaction_type == "Thu nhập":
                    self.wallet.balance -= old.amount
                else:
                    self.wallet.balance += old.amount
                
                # Cộng giao dịch mới
                if self.transaction_type == "Thu nhập":
                    self.wallet.balance += self.amount
                else:
                    self.wallet.balance -= self.amount
                
                self.wallet.save()
        else:  # Giao dịch mới
            if self.transaction_type == "Thu nhập":
                self.wallet.balance += self.amount
            else:
                self.wallet.balance -= self.amount
            self.wallet.save()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # khi xóa giao dịch thì hoàn lại số dư
        if self.transaction_type == "Thu nhập":
            self.wallet.balance -= self.amount
        elif self.transaction_type == "Chi tiêu":
            self.wallet.balance += self.amount

        self.wallet.save()
        super().delete(*args, **kwargs) 

    
class Budget(models.Model):
    REPEAT_CHOICES = [
        ('none', 'Không lặp lại'),
        ('daily', 'Hằng ngày'),
        ('weekly', "Hằng tuần"),
        ('monthly', "Hằng tháng"),
        ('yearly', 'Hằng năm'),
    ]
    user = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE, related_name='budgets')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='monthly')

    class Meta:
        # ràng buộc trong bảng Budget không được xuất hiện 2 bản ghi có cùng user, category, month
        unique_together = ('user', 'wallet', 'category' ,'start_date')
        verbose_name_plural = 'Budgets' 

    def __str__(self):
        return f"{self.category.name} - {self.start_date.strftime('%m/%Y')}"
    
    # Xác định khoảng thời gian của chu kỳ hiện tại
    def get_current_cycle(self):
        from datetime import timedelta
        import calendar
        from django.utils import timezone
        today = timezone.now().date()

        # Nếu ngân sách chưa bắt đầu, chu kỳ hiện tại là chu kỳ đầu tiên
        if today < self.start_date:
            ref_date = self.start_date
            is_future = True
        else:
            ref_date = today
            is_future = False

        if self.repeat == 'daily':
            return ref_date, ref_date

        elif self.repeat == 'weekly':
            if is_future:
                return self.start_date, self.start_date + timedelta(days=6)
            else:
                weeks_passed = (today - self.start_date).days // 7
                current_start = self.start_date + timedelta(weeks=weeks_passed)
                return current_start, current_start + timedelta(days=6)

        elif self.repeat == 'monthly':
            if is_future or (today.year == self.start_date.year and today.month == self.start_date.month):
                current_start = self.start_date
            else:
                current_start = ref_date.replace(day=1)
            _, last_day = calendar.monthrange(ref_date.year, ref_date.month)
            current_end = ref_date.replace(day=last_day)
            return current_start, current_end

        elif self.repeat == 'yearly':
            if is_future or today.year == self.start_date.year:
                current_start = self.start_date
            else:
                current_start = ref_date.replace(month=1, day=1)
            current_end = ref_date.replace(month=12, day=31)
            return current_start, current_end

        else: # none (Không lặp lại)
            return self.start_date, self.start_date

    # Tính tổng số ngày của chu kỳ hiện tại
    def cycle_days(self):
        start, end = self.get_current_cycle()
        return (end - start).days + 1

    # Tính tổng đã chi trong chu kỳ hiện tại
    def spent(self):
        from django.db.models import Sum
        start, end = self.get_current_cycle()
        result = Transaction.objects.filter(
            user=self.user,
            wallet=self.wallet,
            category=self.category,
            transaction_type='Chi tiêu',
            date__gte=start,
            date__lte=end
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return result

    # Số tiền còn lại
    def remaining(self):
        return self.amount - self.spent()

    # Tính phần trăm đã chi
    def percent_spent(self):
        if self.amount == 0:
            return 0
        return round((self.spent() / self.amount) * 100, 1)
    
    # Số ngày còn lại trong chu kỳ
    def days_remaining(self):
        from django.utils import timezone
        today = timezone.now().date()
        start, end = self.get_current_cycle()
        
        if today > end:
            return 0
        if today < start:
            return self.cycle_days()
            
        delta = (end - today).days + 1
        return max(delta, 0)
    
    # Mỗi ngày nên chi
    def should_spend_per_day(self):
        days = self.cycle_days()
        if days == 0:
            return 0
        return round(self.amount / days, 0)

    # Mỗi ngày còn lại nên chi
    def remaining_per_day(self):
        days = self.days_remaining()
        if days == 0:
            return 0
        return round(self.remaining() / days, 0)

    @classmethod
    def total_summary(cls, user):
        budget = cls.objects.filter(user=user)
        # Cách viết pythonic
        total_amount = sum(b.amount for b in budget)
            # cách viết tường minh
            # total_amount = 0
            # for b in budget:
            #     total_amount += b.amount
        total_spent = sum(b.spent() for b in budget)
        total_remaining = total_amount - total_spent
        return {
            'total_amount': total_amount,
            'total_spent': total_spent,
            'total_remaining': total_remaining,
            'percent_spent': round((total_spent / total_amount) * 100, 1) if total_amount else 0,
        }

# tính toán cho biểu đồ
class ReportService:
    def __init__(self, user, month, year, wallet=None):
        self.user = user
        self.month = month
        self.year = year
        self.transactions = Transaction.objects.filter(
            user=user,
            date__month=month,
            date__year=year
        )
        # chọn ví
        if wallet:
            self.transactions = self.transactions.filter(wallet=wallet)
        
    # tổng thu
    def total_income(self):
        return self.transactions.filter(transaction_type='Thu nhập').aggregate(Sum('amount'))['amount__sum'] or 0

    # tổng chi
    def total_expense(self):
        return self.transactions.filter(transaction_type='Chi tiêu').aggregate(Sum('amount'))['amount__sum'] or 0

    # tiết kiệm
    def total_saving(self):
        return self.total_income() - self.total_expense()
    
    # top danh muc chi nhieu nhat
    def top_expense_categories(self, limit=5):
        return self.transactions.filter(transaction_type='Chi tiêu').values('category__name', 'category__icon').annotate(total=Sum('amount')).order_by('-total')[:limit]
    
    # so sánh tháng trước
    def compare_with_last_month(self):
        if self.month == 1:
            last_month, last_year = 12, self.year - 1
        else:
            last_month, last_year = self.month - 1, self.year

        last = ReportService(self.user, last_month, last_year)
        return {
            'income_diff': self.total_income() - last.total_income(),
            'expense_diff': self.total_expense() - last.total_expense(),
            'saving_diff': self.total_saving() - last.total_saving(), 
        } 
    
    # thu chi theo từng ngày trong tháng (cho biểu đồ)
    def daily_summary(self):
        from django.db.models.functions import TruncDay
        # day=TruncDay('date')): cắt datetime xuống mức ngày
        # values('day', 'transaction_type'): lấy ra ngày + loại giao dịch
        # annotate(total=Sum('amount')): tính tổng tiền cho mỗi nhóm
        # order_by('day'): sắp xếp theo ngày
        return self.transactions.annotate(day=TruncDay('date')).values('day', 'transaction_type').annotate(total=Sum('amount')).order_by('day')
