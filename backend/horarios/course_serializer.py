# serializers/course_serializer.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    curriculum_year = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'academic_year_level', 'curriculum_year']
        depth = 1  # suficiente para acceder academic_year_level

    def get_curriculum_year(self, obj):
        return obj.curriculum.year  # suponiendo que la FK se llama 'curriculum'
