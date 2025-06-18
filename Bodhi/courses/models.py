from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from utils.choices import *
from accounts.managers import CustomUserManager,ActiveManager
import uuid


class Category(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=254, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categorys"

    def __str__(self):
        return str(self.name)
    
class Level(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=254, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Levels"

    def __str__(self):
        return str(self.name)
    

class Courses(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=254, null=True, blank=True)
    course_id = models.CharField(max_length=254, unique=True,null=True, blank=True, verbose_name='Course UID')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_assessment_required = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                related_name='course_category',null=True, blank=True)
    level = models.ManyToManyField(
        Level, blank=True,related_name='course_level')
    
    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return str(self.name)
    

class CourseDetails(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    course_detail_id = models.CharField(max_length=254, unique=True,null=True, blank=True, verbose_name='Course Detail UID')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    level_type = models.ForeignKey(Level, on_delete=models.CASCADE,
                related_name='course_details_level',null=True, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,
                related_name='course_details',null=True, blank=True)
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "CourseDetails"

    def __str__(self):
        return str(self.object_id)
    

class Module(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=254, null=True, blank=True)
    module_id = models.CharField(max_length=254,unique=True, null=True, blank=True, verbose_name='Module UID')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    course_details = models.ForeignKey(CourseDetails, on_delete=models.CASCADE,
                related_name='course_details_module',null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "Modules"

    def __str__(self):
        return str(self.name)
    

class Lesson(AuditFields):
    object_id = models.UUIDField(
        unique=True,null=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=254, null=True, blank=True)
    lesson_id = models.CharField(max_length=254,unique=True, null=True, blank=True, verbose_name='Lesson UID')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                related_name='module_lesson',null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "Lessons"

    def __str__(self):
        return str(self.name)
    

