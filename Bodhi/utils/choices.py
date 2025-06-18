from django.db import models
from django.conf import settings
from django.db.models import Q


USER_ROLE_CHOICES = (
    ("SUPER ADMIN", "SUPER ADMIN"),
    ("TUTOR", "TUTOR"),
    ("STUDENT", "STUDENT")
)

TYPE_LOGIN_CHOICES = (
    ('OTP', 'OTP'),
    ('PASSWORD', 'PASSWORD'),
)


LEVELS = (
    ('BEGINER', 'BEGINER'),
    ('INTERMEDIATE', 'INTERMEDIATE'),
    ('EXPERT', 'EXPERT'),
)


class AuditFields(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
