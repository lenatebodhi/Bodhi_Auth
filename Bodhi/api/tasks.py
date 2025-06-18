from celery import shared_task
from django.core.mail import send_mail
from Bodhi.settings import *
from django.template.loader import render_to_string


@shared_task
def send_email(subject,message,email):
    print("inside celery")
    send_mail(
        subject,
        message ,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )