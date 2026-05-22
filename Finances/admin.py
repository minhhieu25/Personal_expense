from django.contrib import admin
from .models import Budget, Transaction, Category
# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
