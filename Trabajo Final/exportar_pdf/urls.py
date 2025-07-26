from django.urls import path
from .views import exportar_horarios_pdf

urlpatterns = [
    path('exportar-horarios/', exportar_horarios_pdf, name='exportar_horarios_pdf'),
]