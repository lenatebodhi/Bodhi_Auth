from django.contrib import admin
from courses.models import *

# Register your models here.
admin.site.register(Courses)
admin.site.register(Module)
admin.site.register(Lesson)

admin.site.register(Category)
admin.site.register(Level)

admin.site.register(CourseDetails)
