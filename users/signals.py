from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if instance.email:
        send_mail(
            "Welcome to Goodreads Clone website",
            f"Hello {instance.first_name}, welcome to Goodreads Clone website. We hope you enjoy our website.",
            "umirzokovakbar@gmail.com",
            [instance.email],

        )
