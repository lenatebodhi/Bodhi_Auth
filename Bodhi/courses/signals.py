from courses.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Courses)
def course_code_created(sender, instance, created, **kwargs):
    
    print("h0")
    if created:
        print("hi")
        course_id = f"ID-{instance.id}"
        instance.course_id = course_id
        instance.save()

@receiver(post_save, sender=Module)
def module_code_created(sender, instance, created, **kwargs):
    
    if created:
        module_id = f"ID-{instance.id}"
        instance.module_id = module_id
        instance.save()

@receiver(post_save, sender=Lesson)
def lesson_code_created(sender, instance, created, **kwargs):
    
    if created:
        lesson_id = f"ID-{instance.id}"
        instance.lesson_id = lesson_id
        instance.save()