from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from recuperar_contrasena.views import recuperacion
from horarios.views import (
    UserViewSet, GroupViewSet, AcademicUnitViewSet, CurriculumViewSet, 
    TermViewSet, AcademicYearLevelViewSet, ClassroomViewSet, ScheduleVersionViewSet,
    SessionViewSet, GlobalConstraintViewSet, ProfessorCreateView
)
from horarios.professor_view import ProfessorUpdateView, ProfessorListView  # Importa la vista de actualización del profesor
from horarios.course_view import CourseListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
import login.urls
from horarios.schedule_view import GenerarHorarioView, obtener_horarios_por_anio


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'academic-units', AcademicUnitViewSet)
router.register(r'curricula', CurriculumViewSet)
router.register(r'terms', TermViewSet)
router.register(r'year-levels', AcademicYearLevelViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'schedule-versions', ScheduleVersionViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'global-constraints', GlobalConstraintViewSet)

urlpatterns = [
    path('admin/',admin.site.urls),
    path('api/', include(router.urls)),
    path('api/profesores/', ProfessorCreateView.as_view(), name='crear_profesor'),
    path('api/profesores/<int:pk>/', ProfessorUpdateView.as_view(), name='actualizar_profesor'),
    path('api/cursos/', CourseListView.as_view(), name='lista-cursos'),
    path('api/', include(login.urls)),
    path('api/listar-profesores/', ProfessorListView.as_view(), name='listar-profesores'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/recuperarContrasena/', recuperacion, name='recuperacion'),
    path('api/generar-horario/', GenerarHorarioView.as_view(), name='generar_horario'),
    path('api/horarios/', obtener_horarios_por_anio, name='ver-horarios'),
    path('api/', include('exportar_pdf.urls')),
    
]

