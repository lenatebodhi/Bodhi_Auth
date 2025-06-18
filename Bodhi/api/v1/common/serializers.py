import re
from django.core.validators import FileExtensionValidator, RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import *


class InterestDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'title']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'
