from rest_framework import serializers
from django.contrib.auth.models import User, Group
from horarios.models import (
    AcademicUnit, Curriculum, Term,
    AcademicYearLevel, Course, CourseGroup, Classroom,
    ScheduleVersion, Session, GlobalConstraint
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class AcademicUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicUnit
        fields = '__all__'

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class AcademicYearLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYearLevel
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'academic_unit', 'curriculum', 'term', 'year']

        fields = '__all__'

class CourseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGroup
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class ScheduleVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleVersion
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class GlobalConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalConstraint
        fields = '__all__'
