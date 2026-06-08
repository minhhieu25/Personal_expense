from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_verification_email(user, request):
    from .models import EmailVerification

    # Tạo/lấy token
    verification, _ = EmailVerification.objects.get_or_create(user=user)

    # Tạo link xác thực
    url_path = reverse('users:verify_email', kwargs={'token': verification.token})

    link  = request.build_absolute_uri(url_path)   

    send_mail(
        subject = 'Xác thực tài khoản',
        message = f'Bấm vào link để xác thực tài khoản: {link}',
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [user.email],
    )

