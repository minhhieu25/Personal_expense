from Finances.models import Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def ceate_default_categories(sender, instance, created, **kwargs):
    # Tự động tạo category mặc định khi user được tạo mới (created = True)
    if created: # chỉ chạy khi user mới được tạo, không chạy khi update
        default_categories = [
            # thu nhập
            {'name': 'Lương', 'type': 'Thu nhập', 'icon': '💰'},
            {'name': 'Thưởng', 'type': 'Thu nhập', 'icon': '🎁'},
            {'name': 'Frelance', 'type': 'Thu nhập', 'icon': '💻'},
            {'name': 'Khác (thu)', 'type': 'Thu nhập', 'icon': '📌'},
            
            # Chi tiêu
            {'name': 'Ăn uống', 'type': 'Chi tiêu', 'icon': '🍔'},
            {'name': 'Học phí', 'type': 'Chi tiêu', 'icon': '📚'},
            {'name': 'Đi lại', 'type': 'Chi tiêu', 'icon': '🚗'},
            {'name': 'Điện nước', 'type': 'Chi tiêu', 'icon': '💡'},
            {'name': 'Intenet', 'type': 'Chi tiêu', 'icon': '🌐'},
            {'name': 'Mua sắm', 'type': 'Chi tiêu', 'icon': '🛍️'},
            {'name': 'Giải trí', 'type': 'Chi tiêu', 'icon': '🎮'},
            {'name': 'Khác (Chi)', 'type': 'Chi tiêu', 'icon': '📌'},
        ]

        for i in default_categories:
            Category.objects.create(
                user = instance,
                name = i['name'],
                type = i['type'],
                icon = i['icon'],
            )

