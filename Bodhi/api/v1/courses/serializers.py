import re
from django.core.validators import FileExtensionValidator, RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from courses.models import *

class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        fields = ["id","name"]

class LevelSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Level
        fields = ["id","name"]

class ModuleCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Module
        fields = "__all__"


class LessonCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Lesson
        fields = "__all__"
        

class CourseCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Courses
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    level = LevelSerializer(required=False,many=True)
   
    class Meta:
        model = Courses
        fields = "__all__"


class CourseDetailsCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CourseDetails
        fields = "__all__"


class CourseDetailsSerializer(serializers.ModelSerializer):
    level_type = LevelSerializer(required=False)
    course = CourseSerializer(required=False)

   
    class Meta:
        model = CourseDetails
        fields = "__all__"


class ModuleDeatilSerializer(serializers.ModelSerializer):
    course_details = CourseDetailsSerializer(required=False,read_only=True)

   
    class Meta:
        model = Module
        fields = "__all__"


class LessonDetailSerializer(serializers.ModelSerializer):
    module = ModuleDeatilSerializer(required=False,read_only=True)

   
    class Meta:
        model = Lesson
        fields = "__all__"