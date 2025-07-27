import random
from datetime import time
from django.db import transaction
from django.db.models import Max
from .models import (
    Term, Curriculum, ScheduleVersion, Professor, CourseGroup,
    Classroom, Session, AcademicYearLevel
)

DAY = [(0, "Lunes"), (1, "Martes"), (2, "Miércoles"), (3, "Jueves"), (4, "Viernes")]
TIME_BLOCKS = [
    (time(7, 0), time(7, 50)), (time(7, 50), time(8, 40)), (time(8, 50), time(9, 40)),
    (time(9, 40), time(10, 30)), (time(10, 40), time(11, 30)), (time(11, 30), time(12, 20)),
    (time(12, 20), time(13, 10)), (time(14, 0), time(14, 50)), (time(14, 50), time(15, 40)),
    (time(15, 50), time(16, 40)), (time(16, 40), time(17, 30)), (time(17, 30), time(18, 20)),
    (time(18, 30), time(19, 20)), (time(19, 20), time(20, 10)),
]
SHIFT_BLOCK_RANGES = {'M': (0, 6), 'T': (7, 13)}

def _split_hours(total_hours: int) -> list[int]:
    if total_hours <= 0: return []
    if total_hours == 3: return [3]
    sessions, remaining = [], total_hours
    while remaining > 0:
        if remaining >= 3 and remaining != 4: sessions.append(3); remaining -= 3
        else: sessions.append(2); remaining -= 2
    return sorted(sessions, reverse=True)

def _place_group_intelligently(group, profesores, aulas, aulas_pref, aula_comodin, ocup_prof, ocup_aula, cursos_C):
    curso = group.course
    bloques_requeridos = _split_hours(curso.ht + curso.htp + curso.hp)
    prof_list = [p for p in profesores if curso in p.can_teach_courses.all()] or [None]
    
    num_bloques = len(bloques_requeridos)
    if num_bloques == 0:
        return []
    
    mejor_asignacion_global = None
    mejor_score_global = float('inf')

    for prof in prof_list:
        asignacion = _find_assig_backtrack(
            bloques_requeridos, prof, group, aulas, aulas_pref, aula_comodin, ocup_prof, ocup_aula
        )
        
        if asignacion:
            dias_usados = [a['dia'] for a in asignacion]
            consecutive_penalty = _count_consecutive_days(dias_usados) * 20
            score_base_total = sum(a.get('score_base', 0) for a in asignacion)
            score_total = score_base_total + consecutive_penalty
            
            if score_total < mejor_score_global:
                mejor_score_global = score_total
                mejor_asignacion_global = asignacion
                
                if consecutive_penalty == 0:
                    break

    if mejor_asignacion_global:
        for asignacion in mejor_asignacion_global:
            if asignacion['prof']:
                ocup_prof[asignacion['prof'].id][asignacion['dia']].update(asignacion['indices'])
            ocup_aula[asignacion['aula'].id][asignacion['dia']].update(asignacion['indices'])
        
        return mejor_asignacion_global
    
    return None

def _count_consecutive_days(dias_list):
    if len(dias_list) <= 1:
        return 0
    sorted_days = sorted(dias_list)
    consecutive_count = 0
    for i in range(len(sorted_days) - 1):
        if sorted_days[i+1] - sorted_days[i] == 1:
            consecutive_count += 1
    return consecutive_count


def _find_assig_backtrack(bloques_requeridos, prof, group, aulas, aulas_pref, aula_comodin, ocup_prof, ocup_aula):

    def backtrack(bloque_idx, asignacion_parcial, ocupaciones_temp_prof, ocupaciones_temp_aula, dias_usados_grupo):
        
        if bloque_idx >= len(bloques_requeridos):
            return asignacion_parcial.copy()
        
        duracion = bloques_requeridos[bloque_idx]
        
        opciones = []
        for dia_idx, _ in DAY:

            if dia_idx in dias_usados_grupo:
                continue
                
            start_i, end_i = SHIFT_BLOCK_RANGES[group.shift]
            
            for i in range(start_i, end_i - duracion + 1):
                indices = set(range(i, i + duracion))
                
                if prof:
                    if not ocup_prof[prof.id][dia_idx].isdisjoint(indices):
                        continue
                
                # Buscar aulas disponibles
                aula_preferente = aulas_pref.get(group.academic_year_level.year_level)
                aulas_a_revisar = ([aula_preferente] if aula_preferente else []) + \
                                ([aula_comodin] if aula_comodin else []) + aulas
                
                for aula in aulas_a_revisar:
                    # Verificar disponibilidad del aula en el horario GLOBAL
                    if aula and not ocup_aula[aula.id][dia_idx].isdisjoint(indices):
                        continue
                    
                    # Calcular score para esta opción
                    score = 0
                    if aula != aula_preferente: score += 10
                    if aula == aula_comodin: score += 20
                    if i < 2: score += 5
                    if i > end_i - 3: score += 5
                    
                    # Bonificar días que evitan consecutivos con días ya asignados
                    dias_ya_usados = list(dias_usados_grupo)
                    if dias_ya_usados:
                        es_consecutivo = any(abs(dia_idx - dia_usado) == 1 for dia_usado in dias_ya_usados)
                        if es_consecutivo:
                            score += 15  # Penalización moderada por consecutivo
                    
                    opciones.append({
                        'prof': prof, 'aula': aula, 'dia': dia_idx,
                        'start_index': i, 'indices': indices, 'duracion': duracion,
                        'score_base': score
                    })
                    break 
        
        opciones.sort(key=lambda x: x['score_base'])
        
        for opcion in opciones:

            nuevos_dias_usados = dias_usados_grupo | {opcion['dia']}
            
            nueva_asignacion = asignacion_parcial + [opcion]
            resultado = backtrack(bloque_idx + 1, nueva_asignacion, ocupaciones_temp_prof, ocupaciones_temp_aula, nuevos_dias_usados)
            
            if resultado is not None:
                return resultado
        
        return None

    return backtrack(0, [], {}, {}, set())



def _generation_attempt(grupos, profesores, aulas, aulas_pref, aula_comodin, cursos_C, repair_iterations=5):

    ocup_prof = {p.id: {d[0]: set() for d in DAY} for p in profesores}
    ocup_aula = {a.id: {d[0]: set() for d in DAY} for a in aulas}
    
    sesiones_confirmadas, grupos_no_programados = [], []
    grupos_ordenados = sorted(grupos, key=lambda g: g.course.ht + g.course.htp + g.course.hp, reverse=True)
    
    for grp in grupos_ordenados:
        asignaciones = _place_group_intelligently(grp, profesores, aulas, aulas_pref, aula_comodin, ocup_prof, ocup_aula, cursos_C)
        if asignaciones:
            dias_asignados = [a['dia'] for a in asignaciones]
            
            if len(set(dias_asignados)) != len(dias_asignados):
                grupos_no_programados.append(grp)
                continue
            
            for a in asignaciones:
                sesiones_confirmadas.append({
                    'grupo': grp, 'profesor': a['prof'], 'aula': a['aula'], 
                    'dia': a['dia'], 'hora_inicio': TIME_BLOCKS[a['start_index']][0], 
                    'duracion': a['duracion'], 'indices': a['indices']
                })
        else:
            grupos_no_programados.append(grp)
    
    if grupos_no_programados:
        for dia_idx, dia_nom in DAY:
            ocupacion_dia = set()
            for p_id, dias_prof in ocup_prof.items():
                ocupacion_dia.update(dias_prof[dia_idx])
            for a_id, dias_aula in ocup_aula.items():
                ocupacion_dia.update(dias_aula[dia_idx])
            
            bloques_libres = set(range(14)) - ocupacion_dia
    
    if not grupos_no_programados: return sesiones_confirmadas, []

    for i in range(repair_iterations):
        if not grupos_no_programados: break
        
        divisor = max(4 - i, 1) 
        num_a_arrancar = min(len(sesiones_confirmadas) // divisor, 15) 
        grupos_en_horario = list({s['grupo'] for s in sesiones_confirmadas})
        random.shuffle(grupos_en_horario)
        grupos_a_reintentar = grupos_no_programados + grupos_en_horario[:num_a_arrancar]
        ids_a_reintentar = {g.id for g in grupos_a_reintentar}

        nuevas_sesiones = []
        for s in sesiones_confirmadas:
            if s['grupo'].id in ids_a_reintentar:
                if s['profesor']: ocup_prof[s['profesor'].id][s['dia']].difference_update(s['indices'])
                ocup_aula[s['aula'].id][s['dia']].difference_update(s['indices'])
            else: nuevas_sesiones.append(s)
        sesiones_confirmadas = nuevas_sesiones
        
        grupos_a_reintentar.sort(key=lambda g: g.course.ht + g.course.htp + g.course.hp, reverse=True)
        random.shuffle(grupos_a_reintentar) 
        
        grupos_no_programados = []
        for grp in grupos_a_reintentar:
            asignaciones = _place_group_intelligently(grp, profesores, aulas, aulas_pref, aula_comodin, ocup_prof, ocup_aula, cursos_C)
            if asignaciones:
                dias_asignados = [a['dia'] for a in asignaciones]
                
                if len(set(dias_asignados)) != len(dias_asignados):
                    grupos_no_programados.append(grp)
                    continue
                
                for a in asignaciones:
                    if a['prof']: ocup_prof[a['prof'].id][a['dia']].update(a['indices'])
                    ocup_aula[a['aula'].id][a['dia']].update(a['indices'])
                    sesiones_confirmadas.append({
                        'grupo': grp, 'profesor': a['prof'], 'aula': a['aula'], 
                        'dia': a['dia'], 'hora_inicio': TIME_BLOCKS[a['start_index']][0], 
                        'duracion': a['duracion'], 'indices': a['indices']
                    })
            else: grupos_no_programados.append(grp)
                
    return sesiones_confirmadas, [{"grupo": f"{g.course.name} - {g.group_code}", "motivo": "No se encontró combinación en fase de reparación."} for g in grupos_no_programados]

def generate_schedule(term_id: int, mallas_por_año: dict[int, int], cursos_con_seccion_C: list[int], created_by: str, max_attempts: int = 15) -> tuple[ScheduleVersion | None, list]:
    try: term = Term.objects.get(id=term_id)
    except Term.DoesNotExist: 
        print(f"El período académico con ID {term_id} no existe.")
        return None, []

    profesores = list(Professor.objects.prefetch_related("availabilities", "can_teach_courses").order_by("id"))
    aulas = list(Classroom.objects.all())
    if not aulas: 
        print("No hay aulas disponibles para agendar sesiones.")
        return None, []
    aulas_preferentes = {a.year_preference: a for a in aulas if a.year_preference}
    aula_comodin = next((a for a in aulas if a.short_code == "205"), None)

    for year_str, malla in mallas_por_año.items():
        grupos_a_agendar = []
        
        try:
            nivel = AcademicYearLevel.objects.get(year_level=int(year_str), semester_number=term.id)
            print("Obteniendo grupos para el año:", year_str, "y malla:", malla, "con nivel:", nivel)
            curriculum = Curriculum.objects.get(year=malla)
            grupos_a_agendar.extend(list(CourseGroup.objects.filter(course__term=term, course__curriculum=curriculum, academic_year_level=nivel).select_related("course", "academic_year_level")))
            for grupo in grupos_a_agendar:
                print (f"Grupo encontrado: {grupo.course.name} - {grupo.group_code}")
        except Exception: print(f"Error al obtener grupos para el año {year_str} y malla {malla}.")

    best_sessions, best_unplaced = [], [{'id': i} for i in range(len(grupos_a_agendar) + 1)]

    for intento in range(max_attempts):
        random.shuffle(grupos_a_agendar)
        sesiones, unplaced = _generation_attempt(grupos_a_agendar, profesores, aulas, aulas_preferentes, aula_comodin, cursos_con_seccion_C)
        
        if not unplaced:
            best_sessions, best_unplaced = sesiones, []
            break
        if len(unplaced) < len(best_unplaced):
            best_sessions, best_unplaced = sesiones, unplaced

    if not best_sessions:
        print("No se pudo generar un horario válido en ninguno de los intentos.")
        return None, best_unplaced

    last_ver = ScheduleVersion.objects.filter(term=term).aggregate(Max("version_number"))["version_number__max"] or 0
    schedule_version = ScheduleVersion.objects.create(term=term, version_number=last_ver + 1, created_by=created_by, notes=f"Automático optimizado con distribución inteligente. {len(best_unplaced)} cursos sin agendar.")
    
    try:
        with transaction.atomic():
            Session.objects.filter(version__term=term).delete()
            Session.objects.bulk_create([
                Session(course_group=s['grupo'], version=schedule_version, professor=s['profesor'], classroom=s['aula'], day=s['dia'], start_time=s['hora_inicio'], duration_blocks=s['duracion'], session_type="theory") for s in best_sessions
            ])
        
        schedule_version.state = 'review'; schedule_version.save()
    except Exception as e:
        print(f"Error al guardar el horario: {e}")
        schedule_version.delete()
        return None, best_unplaced

    return schedule_version, best_unplaced