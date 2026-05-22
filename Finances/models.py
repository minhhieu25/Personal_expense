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
        return f"Số dư: {self.balance:,.0f} VNĐ"

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
    
    def save(self, *args, **kwargs):
        if self.pk: # khi da ton tai giao dich (co pk)
            old = Transaction.objects.get(pk=self.pk)

            # hoan lai tien cua vi cu
            if old.transaction_type == "Thu nhập":
                old.wallet.balance -= old.amount
            elif old.transaction_type == "Chi tiêu":   
                old.wallet.balance += old.amount

            # neu thay doi vi, luu vi cu
            if old.wallet != self.wallet:
                old.wallet.save()

            # cap nhat tien cua vi moi
            if self.transaction_type == "Thu nhập":
                self.wallet.balance += self.amount
            elif self.transaction_type == "Chi tiêu":
                self.wallet.balance -= self.amount

            self.wallet.save()
        else: # khi co giao dich moi
            if self.transaction_type == "Thu nhập":
                self.wallet.balance += self.amount
            elif self.transaction_type == "Chi tiêu":
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
    
    # Tinh tong da chi
    def spent(self):
        result = Transaction.objects.filter(
            user=self.user,
            wallet=self.wallet,
            category=self.category,
            transaction_type='Chi tiêu',
            date__month=self.start_date.month,
            date__year=self.start_date.year
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return result

    # So tien con lai
    def remaining(self):
        return self.amount - self.spent()

    # Tinh phan tram da chi
    def percent_spent(self):
        if self.amount == 0:
            return 0
        return round((self.spent() / self.amount) * 100, 1)
    
    # Số ngày trong tháng
    def days_in_month(self):
        return calendar.monthrange(self.start_date.year, self.start_date.month)[1]
    
    # Số ngày còn lại trong tháng
    def days_remaining(self):
        today = timezone.now().date()
        end_of_month = self.start_date.replace(day=self.days_in_month())
        delta = (end_of_month - today).days
        return max(delta, 0) # khong tra ve so am
    
    # Mỗi ngày nên chi
    def should_spend_per_day(self):
        if self.days_in_month() == 0:
            return 0
        return round(self.amount / self.days_in_month(), 0)

    # Mỗi ngày còn lại nên chi
    def remaining_per_day(self):
        if self.days_remaining() == 0:
            return 0
        return round(self.remaining() / self.days_remaining(), 0)
    
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

