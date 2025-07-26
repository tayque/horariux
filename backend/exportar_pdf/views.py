from horarios.models import Session, AcademicYearLevel, ScheduleVersion
from horarios.models.classroom import Classroom
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import pprint

def exportar_horarios_pdf(request):
    anios = ['1° año', '2° año', '3° año', '4° año', '5° año', 'Reprogramados']
    year_map = {
        '1° año': 1,
        '2° año': 2,
        '3° año': 3,
        '4° año': 4,
        '5° año': 5
    }
    
    horarios_base = [
        '07:00', '07:50', '08:50', '09:40', '10:40', '11:30', '12:20', '13:10',
        '14:00', '14:50', '15:50', '16:40', '17:30', '18:30', '19:20'
    ]
    
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
    day_map = {0: 'lunes', 1: 'martes', 2: 'miercoles', 3: 'jueves', 4: 'viernes'}

    def hora_a_minutos(hora):
        h, m = hora.split(':')
        return int(h) * 60 + int(m)

    def encontrar_indice_hora(hora_inicio):
        minutos_inicio = hora_a_minutos(hora_inicio)
        horarios_minutos = [
            420, 470, 530, 580, 640, 690, 740, 790,  # 07:00 - 13:10
            840, 890, 950, 1000, 1050, 1110, 1160    # 14:00 - 19:20
        ]
        try:
            return horarios_minutos.index(minutos_inicio)
        except ValueError:
            return -1

    datos_estructurados = {}
    
    for anio in anios:
        if anio in year_map:

            horario_anio = []
            for i, hora in enumerate(horarios_base):
                fila = {
                    'hora': f"{hora} - {horarios_base[i+1] if i < len(horarios_base)-1 else '20:10'}",
                    'hora_inicio': hora
                }
                for dia in dias:
                    fila[dia] = {'curso': '', 'duracion': 1, 'es_primer_bloque': True}
                horario_anio.append(fila)

            version_activa = ScheduleVersion.objects.filter(
                state__in=['final', 'approved', 'review', 'draft']
            ).order_by('-created_at').first()
            
            if version_activa:
                sesiones = Session.objects.filter(
                    course_group__course__academic_year_level__year_level=year_map[anio],
                    version=version_activa
                )
                
                for sesion in sesiones:
                    hora_str = sesion.start_time.strftime('%H:%M')
                    dia_str = day_map.get(sesion.day)
                    duracion = sesion.duration_blocks
                    
                    if dia_str in dias:
                        indice_inicio = encontrar_indice_hora(hora_str)
                        
                        if indice_inicio != -1:

                            for i in range(duracion):
                                indice = indice_inicio + i
                                if indice < len(horario_anio):
                                    horario_anio[indice][dia_str] = {
                                        'curso': sesion.course_group.course.name,
                                        'duracion': duracion,
                                        'es_primer_bloque': i == 0
                                    }
            
            datos_estructurados[anio] = horario_anio

    aulas = {}
    for anio, year_num in year_map.items():
        aula = Classroom.objects.filter(year_preference=year_num).first()
        if aula and aula.full_code:
            partes = aula.full_code.split()
            numero = partes[-1] if partes else aula.full_code
            aulas[anio] = f"{numero}"
        else:
            aulas[anio] = '—'
    aulas['Reprogramados'] = '—'

    html = render_to_string('exportar_pdf/horarios_pdf.html', {
        'datos_estructurados': datos_estructurados,
        'anios': anios,
        'dias': dias,
        'aulas': aulas,
    })

    nombre_archivo = request.GET.get('nombre', 'horarios.pdf')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"{nombre_archivo}\"'
    
    pisa.CreatePDF(html, dest=response)
    return response