import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from apps.account.models import User
from config.celery import app


@app.task()
def send_mail_reset_passwd(email):
    subject = 'Hi! man'
    user = User.objects.get(email=email)
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = os.getenv('SITE_NAME')
    protocol = os.getenv('PROTOCOL')
    abs_url = f"{protocol}://{current_site}users/api/reset/passwd/{uidb64}/{token}/"
    message = f'Reset Your Password Link:\n {abs_url}'
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email],
              fail_silently=True
              )

    return "Sent"