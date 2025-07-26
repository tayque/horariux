import logging
import random
from datetime import time
from django.db import transaction
from django.db.models import Max
from .models import (
    Term, Curriculum, ScheduleVersion, Professor, CourseGroup,
    Classroom, Session, AcademicYearLevel
)

logger = logging.getLogger(__name__)

DAY = [(0, "Lunes"), (1, "Martes"), (2, "Miércoles"), (3, "Jueves"), (4, "Viernes")]

TIME_BLOCKS = [
    (time(7, 0), time(7, 50)), (time(7, 50), time(8, 40)),
    (time(8, 50), time(9, 40)), (time(9, 40), time(10, 30)),
    (time(10, 40), time(11, 30)), (time(11, 30), time(12, 20)),
    (time(12, 20), time(13, 10)), (time(14, 0), time(14, 50)),
    (time(14, 50), time(15, 40)), (time(15, 50), time(16, 40)),
    (time(16, 40), time(17, 30)), (time(17, 30), time(18, 20)),
    (time(18, 30), time(19, 20)), (time(19, 20), time(20, 10)),
]

SHIFT_BLOCK_RANGES = {'M': (0, 6), 'T': (7, 13)}

def _split_hours(total_hours: int) -> list[int]:
    """Divide las horas totales en bloques de 3 y 2, priorizando los más grandes."""
    if total_hours <= 0:
        return []
    if total_hours == 3:
        return [3]
    sessions, remaining = [], total_hours
    while remaining > 0:
        if remaining >= 3 and remaining != 4:
            sessions.append(3)
            remaining -= 3
        else:
            sessions.append(2)
            remaining -= 2
    return sorted(sessions, reverse=True)


def generate_schedule(term_id: int, mallas_por_año: dict[int, int], cursos_con_seccion_C: list[int], created_by: str, max_attempts: int = 10) -> tuple[ScheduleVersion | None, list]:
    logger.info(f"Inicio de generación de horarios inteligente con hasta {max_attempts} intentos.")

    try:
        term = Term.objects.get(id=term_id)
    except Term.DoesNotExist:
        logger.error(f"Periodo con id={term_id} no encontrado.")
        return None, []

    profesores = list(Professor.objects.prefetch_related("availabilities", "can_teach_courses").order_by("id"))
    aulas = list(Classroom.objects.all())
    aulas_preferentes = {a.year_preference: a for a in aulas if a.year_preference}
    aula_comodin = next((a for a in aulas if a.short_code == "205"), None)

    if not aulas:
        logger.error("No hay aulas registradas. Imposible generar horario.")
        return None, [{"motivo": "No hay aulas disponibles."}]

    grupos_a_agendar = []
    for year_str, malla in mallas_por_año.items():
        year = int(year_str)
        try:
            curriculum = Curriculum.objects.get(year=malla)
            nivel = AcademicYearLevel.objects.get(year_level=year, semester_number=term.id)
            grupos = CourseGroup.objects.filter(
                course__term=term, course__curriculum=curriculum, academic_year_level=nivel
            ).select_related("course", "academic_year_level")
            grupos_a_agendar.extend(list(grupos))
        except Exception:
            logger.warning(f"Configuración faltante para año {year}, malla {malla}.")

    best_sessions, best_unplaced = [], [{'id': i} for i in range(len(grupos_a_agendar)+1)]

    for intento in range(max_attempts):
        random.shuffle(grupos_a_agendar)
        sesiones, unplaced = run_generation_attempt(
            grupos_a_agendar, profesores, aulas, aulas_preferentes, aula_comodin, cursos_con_seccion_C
        )
        if not unplaced:
            best_sessions, best_unplaced = sesiones, []
            logger.info(f"Solución completa en intento {intento+1}.")
            break
        if len(unplaced) < len(best_unplaced):
            best_sessions, best_unplaced = sesiones, unplaced
            logger.info(f"Mejora: {len(unplaced)} cursos sin bloques.")

    if not best_sessions:
        logger.error("No se pudo generar un horario completo.")
        return None, best_unplaced

    last_ver = ScheduleVersion.objects.filter(term=term).aggregate(Max("version_number"))["version_number__max"] or 0
    schedule_version = ScheduleVersion.objects.create(
        term=term, version_number=last_ver+1, created_by=created_by,
        notes=f"Automático inteligente. {len(best_unplaced)} cursos sin agendar."
    )

    try:
        with transaction.atomic():
            objs = []
            for s in best_sessions:
                dia = s['dia']
                aula = s['aula']
                # Log de sesiones en aula comodín
                if aula_comodin and aula.id == aula_comodin.id:
                    logger.info(f"[205] Sesión asignada: grupo={s['grupo'].id}, día={dia}, hora={s['hora_inicio']}")
                objs.append(Session(
                    course_group=s['grupo'], version=schedule_version,
                    professor=s['profesor'], classroom=aula,
                    day=dia, start_time=s['hora_inicio'], duration_blocks=s['duracion'], session_type="theory"
                ))
            Session.objects.bulk_create(objs)
        schedule_version.state = 'review'
        schedule_version.save()
        logger.info(f"Horario v{schedule_version.version_number} guardado exitosamente.")
    except Exception as e:
        logger.error(f"Error al guardar horario: {e}")
        schedule_version.delete()
        return None, best_unplaced

    return schedule_version, best_unplaced


def run_generation_attempt(grupos, profesores, aulas, aulas_pref, aula_com, cursos_C):
    ocup_prof = {p.id: {d[0]: set() for d in DAY} for p in profesores}
    ocup_aula = {a.id: {d[0]: set() for d in DAY} for a in aulas}
    sesiones_conf = []
    no_programados = []

    for grp in grupos:
        curso = grp.course
        total_h = curso.ht + curso.htp + curso.hp
        if total_h == 0 or (grp.group_code == 'C' and curso.id not in cursos_C):
            continue

        bloques = _split_hours(total_h)
        prof_list = [p for p in profesores if curso in p.can_teach_courses.all()] or [None]
        opciones_bloques = []

        for dur in bloques:
            opts = []
            for prof in prof_list:
                for dia_idx, dia_nom in DAY:
                    start_i, end_i = SHIFT_BLOCK_RANGES[grp.shift]
                    for i in range(start_i, end_i - dur + 1):
                        inds = set(range(i, i + dur))
                        if prof:
                            h0, h1 = TIME_BLOCKS[i][0], TIME_BLOCKS[i + dur - 1][1]
                            if not any(av.start_time <= h0 and av.end_time >= h1 for av in prof.availabilities.filter(day=dia_nom)):
                                continue
                            if not ocup_prof[prof.id][dia_idx].isdisjoint(inds):
                                continue
                        for aula in ([aulas_pref.get(grp.academic_year_level.year_level)] + aulas):
                            target_aula = aula or aula_com
                            if not target_aula:
                                continue
                            if not ocup_aula[target_aula.id][dia_idx].isdisjoint(inds):
                                continue
                            opts.append({'prof': prof, 'aula': target_aula, 'dia': dia_idx, 'start': i, 'inds': inds, 'dur': dur})
            if not opts:
                opciones_bloques = []
                break
            random.shuffle(opts)
            opciones_bloques.append(opts)

        asigns, used_days = [], {}
        def bt(idx):
            if idx == len(opciones_bloques):
                return True
            for opt in opciones_bloques[idx]:
                dia = opt['dia']
                # No días consecutivos
                if any(abs(dia - prev) <= 1 for prev in used_days):
                    continue
                asigns.append(opt)
                used_days[dia] = used_days.get(dia, set()) | opt['inds']
                if bt(idx + 1):
                    return True
                used_days[dia] -= opt['inds']
                asigns.pop()
            return False

        if not opciones_bloques or not bt(0):
            no_programados.append({'grupo': f"{curso.name} - {grp.group_code}", 'motivo': 'No espacio para todos los bloques.'})
            continue

        for a in asigns:
            dia, inds, prof, aula = a['dia'], a['inds'], a['prof'], a['aula']
            if prof:
                ocup_prof[prof.id][dia].update(inds)
            ocup_aula[aula.id][dia].update(inds)
            sesiones_conf.append({'grupo': grp, 'profesor': prof, 'aula': aula, 'dia': dia, 'hora_inicio': TIME_BLOCKS[a['start']][0], 'duracion': a['dur']})

    return sesiones_conf, no_programados
