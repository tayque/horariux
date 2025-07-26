import logging
from datetime import datetime, date, time, timedelta
from django.db import transaction
from .models import (
    Term, Curriculum, ScheduleVersion, Professor, CourseGroup,
    Classroom, Session, AcademicYearLevel
)
from django.db.models import Max

logger = logging.getLogger(__name__)

DAY = [(0, "Lunes"), (1, "Martes"), (2, "Miércoles"), (3, "Jueves"), (4, "Viernes")]

def _calculate_end_time_with_recess(start_time: time, duration_blocks: int, shift: str) -> time:
    total_minutes = 50 * duration_blocks
    recess_minutes = 0
    if shift == 'M':
        recess_checkpoints = [time(8, 40), time(10, 30)]
    else:
        recess_checkpoints = [time(15, 40), time(17, 30)]

    current_time = datetime.combine(date.today(), start_time)
    end_time_no_recess = current_time + timedelta(minutes=total_minutes)

    for checkpoint in recess_checkpoints:
        if start_time < checkpoint < end_time_no_recess.time():
            recess_minutes += 10

    final_end_time = current_time + timedelta(minutes=total_minutes + recess_minutes)
    return final_end_time.time()

def _split_hours(total_hours: int) -> list[int]:
    if total_hours <= 0:
        return []
    if total_hours == 3:
        return [3]
    sessions = []
    remaining = total_hours
    while remaining > 0:
        if remaining >= 3 and remaining != 4:
            sessions.append(3)
            remaining -= 3
        else:
            sessions.append(2)
            remaining -= 2
    return sorted(sessions, reverse=True)

def generate_schedule(term_id: int, mallas_por_año: dict[int, int], cursos_con_seccion_C: list[int], created_by: str) -> tuple[ScheduleVersion | None, list]:
    logger.info("Inicio de generación de horarios")
    try:
        term = Term.objects.get(id=term_id)
    except Term.DoesNotExist:
        logger.error("Periodo no encontrado")
        return None, []

    last_version = ScheduleVersion.objects.filter(term=term).aggregate(
        Max("version_number")
    )["version_number__max"] or 0

    new_version_number = last_version + 1

    schedule_version = ScheduleVersion.objects.create(
        term=term,
        version_number=new_version_number,
        created_by=created_by,
        notes="Generación automática de horarios por backend"
    )

    profesores = Professor.objects.prefetch_related("availabilities", "can_teach_courses").order_by("id")
    aulas = Classroom.objects.all()
    aulas_preferentes = {a.year_preference: a for a in aulas if a.year_preference}
    aula_comodin = next((a for a in aulas if a.short_code == "205"), None)

    ocupacion_profesores = {p.id: {d[0]: [] for d in DAY} for p in profesores}
    ocupacion_aulas = {a.id: {d[0]: [] for d in DAY} for a in aulas}

    sesiones_confirmadas = []
    grupos_no_programados = []

    for year_level, malla in mallas_por_año.items():
        print(f"Procesando malla {malla} para el año {year_level}")
        try:
            curriculum = Curriculum.objects.get(year=malla)
        except Curriculum.DoesNotExist:
            logger.warning(f"Malla {malla} no existe")
            continue

        try:
            nivel = AcademicYearLevel.objects.get(
                    year_level=year_level,
                    semester_number=term.id
                )
            print(f"Nivel académico encontrado: {nivel}")
        except AcademicYearLevel.DoesNotExist:
            logger.warning(f"Nivel académico {year_level} no encontrado")
            continue

        grupos = CourseGroup.objects.filter(
            course__term=term,
            course__curriculum=curriculum,
            academic_year_level=nivel
        ).select_related("course", "academic_year_level")
        print(f"Grupos encontrados: {grupos}")
        logger.info(f"Año {year_level}: {grupos.count()} grupos encontrados")

        for grupo in grupos:
            curso = grupo.course
            total_horas = curso.ht + curso.htp + curso.hp
            if total_horas == 0:
                continue

            if grupo.group_code == "C" and curso.id not in cursos_con_seccion_C:
                continue

            posibles_profes = [p for p in profesores if curso in p.can_teach_courses.all()]
            bloques = _split_hours(total_horas)
            
            print(f"Bloques para el grupo {grupo} del curso {curso.name}: {bloques}")
            sesiones_asignadas = []
            exito = True

            for duracion in bloques:
                asignado = False

                for prof in posibles_profes:
                    for disp in sorted(prof.availabilities.all(), key=lambda x: x.day):
                        dia_idx = [d[0] for d in DAY if d[1] == disp.day][0]
                        hora = disp.start_time

                        while _calculate_end_time_with_recess(hora, duracion, grupo.shift) <= disp.end_time:
                            hora_inicio = hora
                            hora_fin = _calculate_end_time_with_recess(hora_inicio, duracion, grupo.shift)

                            if grupo.shift == "M" and hora_inicio >= time(13, 10):
                                break
                            if grupo.shift == "T" and hora_inicio < time(14, 0):
                                hora = time(14, 0)
                                continue

                            prof_busy = any(max(hi, hora_inicio) < min(hf, hora_fin) for hi, hf in ocupacion_profesores[prof.id][dia_idx])
                            aula = aulas_preferentes.get(year_level) or aula_comodin or aulas.first()
                            aula_busy = any(max(hi, hora_inicio) < min(hf, hora_fin) for hi, hf in ocupacion_aulas[aula.id][dia_idx])

                            if not prof_busy and not aula_busy:
                                sesiones_asignadas.append({
                                    "grupo": grupo,
                                    "profesor": prof,
                                    "aula": aula,
                                    "dia": dia_idx,
                                    "hora_inicio": hora_inicio,
                                    "hora_fin": hora_fin,
                                    "duracion": duracion
                                })

                                ocupacion_profesores[prof.id][dia_idx].append((hora_inicio, hora_fin))
                                ocupacion_aulas[aula.id][dia_idx].append((hora_inicio, hora_fin))
                                asignado = True
                                break

                            hora = (datetime.combine(date.today(), hora) + timedelta(minutes=50)).time()

                        if asignado:
                            break
                    if asignado:
                        break

                if not asignado:
                    for dia_idx in range(5):
                        hora = time(7, 0) if grupo.shift == "M" else time(14, 0)
                        hora_limite = time(13, 10) if grupo.shift == "M" else time(20, 10)

                        while _calculate_end_time_with_recess(hora, duracion, grupo.shift) <= hora_limite:
                            hora_inicio = hora
                            hora_fin = _calculate_end_time_with_recess(hora_inicio, duracion, grupo.shift)
                            aula = aulas_preferentes.get(year_level) or aula_comodin or aulas.first()
                            aula_busy = any(max(hi, hora_inicio) < min(hf, hora_fin) for hi, hf in ocupacion_aulas[aula.id][dia_idx])

                            if not aula_busy:
                                sesiones_asignadas.append({
                                    "grupo": grupo,
                                    "profesor": None,
                                    "aula": aula,
                                    "dia": dia_idx,
                                    "hora_inicio": hora_inicio,
                                    "hora_fin": hora_fin,
                                    "duracion": duracion
                                })

                                ocupacion_aulas[aula.id][dia_idx].append((hora_inicio, hora_fin))
                                asignado = True
                                break

                            hora = (datetime.combine(date.today(), hora) + timedelta(minutes=50)).time()

                        if asignado:
                            break

                if not asignado:
                    exito = False
                    break

            if exito:
                sesiones_confirmadas.extend(sesiones_asignadas)
                print(f"Grupo {grupo} programado con {len(sesiones_asignadas)} sesiones.")
            else:
                grupos_no_programados.append({"grupo": grupo, "motivo": "No se pudo asignar horario completo."})
                for s in sesiones_asignadas:
                    if s["profesor"]:
                        ocupacion_profesores[s["profesor"].id][s["dia"]].remove((s["hora_inicio"], s["hora_fin"]))
                    ocupacion_aulas[s["aula"].id][s["dia"]].remove((s["hora_inicio"], s["hora_fin"]))

    if sesiones_confirmadas:
        try:
            with transaction.atomic():
                Session.objects.bulk_create([
                    Session(
                        course_group=s["grupo"],
                        version=schedule_version,
                        professor=s["profesor"] if s["profesor"] else None,
                        classroom=s["aula"],
                        day=s["dia"],
                        start_time=s["hora_inicio"],
                        duration_blocks=s["duracion"],
                        session_type="theory"
                    ) for s in sesiones_confirmadas
                ])
            schedule_version.state = "review"
            schedule_version.save()
        except Exception as e:
            logger.error(f"Error al guardar: {e}")
            schedule_version.delete()
            return None, grupos_no_programados
    else:
        logger.warning("No se generó ninguna sesión")
        schedule_version.delete()
        return None, grupos_no_programados

    return schedule_version, grupos_no_programados
