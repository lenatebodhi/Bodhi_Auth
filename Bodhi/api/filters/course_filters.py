import django_filters
from courses.models import Courses,Module,Lesson


class ModuleFilter(django_filters.FilterSet):
    course_details = django_filters.CharFilter(field_name='course_details',lookup_expr='exact')
    class Meta:
        model = Module
        fields = ['course_details']


class LessonFilter(django_filters.FilterSet):
    module = django_filters.CharFilter(field_name='module',lookup_expr='exact')
    class Meta:
        model = Lesson
        fields = ['module']