# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import time
from .models import Session, AcademicYearLevel
from django.db.models import Q
from .schedule_serializer import HorarioGeneradoInputSerializer
from .models import Term
from .generator import generate_schedule
from .models import ScheduleVersion
from django.db.models import Max

class GenerarHorarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = HorarioGeneradoInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        semester = validated['term_id']
        mallas = validated['mallas_por_año']
        print("Mallas por año:", mallas)
        cursos_c = validated.get('cursos_c', [])
        print("Cursos con sección C:", cursos_c)
        try:
            term = Term.objects.get(id=semester)
        except Term.DoesNotExist:
            return Response({
                "error": f"No se encontró el término académico para el semestre {semester}."
            }, status=status.HTTP_400_BAD_REQUEST)

        created_by = request.user.username if request.user.is_authenticated else "Sistema"
        schedule_version, errores = generate_schedule(
            term_id=semester,
            mallas_por_año=mallas,
            cursos_con_seccion_C=cursos_c,
            created_by=created_by
        )

        if schedule_version:
            return Response({
                "message": "Horario generado exitosamente.",
                "version_id": schedule_version.id
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "No se pudo generar el horario.",
            "errors": errores
        }, status=status.HTTP_400_BAD_REQUEST)

DAYS = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']

@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_horarios_por_anio(request):
    anio_str = request.GET.get('anio')
    
    anio_map = {
        '1° año': 1,
        '2° año': 2,
        '3° año': 3,
        '4° año': 4,
        '5° año': 5,
        'Reprogramados': 0
    }

    year_level = anio_map.get(anio_str)
    if year_level is None:
        return Response({"error": "Año inválido"}, status=400)

    sesiones = Session.objects.filter(
        course_group__academic_year_level__year_level=year_level
    ).select_related("course_group__course")
    
    datos = []
    for s in sesiones:
        datos.append({
            "hora": s.start_time.strftime("%H:%M"),
            "duracion":s.duration_blocks,
            "dia": DAYS[s.day],
            "curso": s.course_group.course.name
        })
    return Response(datos)