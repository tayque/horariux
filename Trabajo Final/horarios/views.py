from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.db import transaction
from horarios.professor_view import ProfessorCreateView
from horarios.models import (
    AcademicUnit, Curriculum, Term,
    AcademicYearLevel, Course, CourseGroup, Classroom,
    ScheduleVersion, Session, GlobalConstraint
)
from horarios.serializers import (
    UserSerializer, GroupSerializer, AcademicUnitSerializer,
    CurriculumSerializer, TermSerializer, AcademicYearLevelSerializer, ClassroomSerializer, 
    ScheduleVersionSerializer, SessionSerializer, GlobalConstraintSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcademicUnitViewSet(viewsets.ModelViewSet):
    queryset = AcademicUnit.objects.all()
    serializer_class = AcademicUnitSerializer
    permission_classes = [permissions.IsAuthenticated]

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    permission_classes = [permissions.IsAuthenticated]

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcademicYearLevelViewSet(viewsets.ModelViewSet):
    queryset = AcademicYearLevel.objects.all()
    serializer_class = AcademicYearLevelSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduleVersionViewSet(viewsets.ModelViewSet):
    queryset = ScheduleVersion.objects.all()
    serializer_class = ScheduleVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

class GlobalConstraintViewSet(viewsets.ModelViewSet):
    queryset = GlobalConstraint.objects.all()
    serializer_class = GlobalConstraintSerializer
    permission_classes = [permissions.IsAuthenticated]

