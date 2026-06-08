from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    currency = models.CharField(max_length=10 ,default="VND")
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2 ,default=0)
    is_verified = models.BooleanField(default=False) # email verification

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from django.utils import timezone
        # token 24h hết hạn
        return (timezone.now() - self.created_at).total_seconds() > 86400