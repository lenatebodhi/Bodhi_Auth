from accounts.managers import ActiveManager, CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.choices import *


class Interest(AuditFields):
    title = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Interests"

    def __str__(self):
        return str(self.title)


class User(AbstractBaseUser, PermissionsMixin, AuditFields):

    user_id = models.CharField(max_length=254, null=True, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    middle_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(_("email"), unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=5, null=True, blank=True)
    phone = models.CharField(max_length=25, unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, null=True, blank=True)
    login_type = models.CharField(max_length=10, choices=TYPE_LOGIN_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    username = models.CharField(max_length=254, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    interests = models.ManyToManyField(Interest, blank=True, null=True, related_name="user_interests")
    otp = models.IntegerField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        """
        Returns the first_name, middle_name (if any), and last_name with spaces.
        Skips any None or empty parts.
        """
        parts = [self.first_name, self.middle_name, self.last_name]
        full_name = " ".join(part for part in parts if part)
        return full_name.strip()



class Education(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educations")
    college = models.CharField(max_length=256)
    degree = models.CharField(max_length=256)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Education"

    def __str__(self):
        return str(self.college)


class Qualification(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="qualifications")
    college = models.CharField(max_length=256)
    degree = models.CharField(max_length=256)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Qualification"

    def __str__(self):
        return str(self.college)


class Achievements(AuditFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Achievements"

    def __str__(self):
        return str(self.title)
