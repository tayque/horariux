
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

DAY = [(0, _("Lunes")), (1, _("Martes")), (2, _("Miércoles")),
       (3, _("Jueves")), (4, _("Viernes"))]

TYPE = [("theory", _("Teoría")), ("htp", _("Teórico‑Práctica")),
        ("practice", _("Práctica")), ("lab", _("Laboratorio")),
        ("seminar", _("Seminario"))]

class Session(models.Model):
    course_group = models.ForeignKey("CourseGroup", on_delete=models.CASCADE,
                                     verbose_name=_("Grupo de curso"))
    version = models.ForeignKey("ScheduleVersion", on_delete=models.CASCADE,
                                verbose_name=_("Versión de horario"))
    professor = models.ForeignKey("Professor", null=True, blank=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=_("Docente"))
    classroom = models.ForeignKey("Classroom", null=True, blank=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=_("Aula"))
    day = models.PositiveSmallIntegerField(choices=DAY,
                                           verbose_name=_("Día"))
    start_time = models.TimeField(verbose_name=_("Hora inicio"))
    duration_blocks = models.PositiveSmallIntegerField(default=1,
                                                       verbose_name=_("Bloques (50 min)"))
    session_type = models.CharField(max_length=10, choices=TYPE,
                                    verbose_name=_("Tipo de sesión"))

    class Meta:
        verbose_name = _("Sesión")
        verbose_name_plural = _("Sesiones")
        unique_together = ("course_group", "version", "day", "start_time")
        ordering = ("day", "start_time")

    @property
    def end_time(self):
        start = datetime.combine(datetime.today(), self.start_time)
        end = start + timedelta(minutes=50 * self.duration_blocks)
        return end.time()

    def __str__(self):
        return f"{self.course_group} – {self.get_day_display()} {self.start_time}"
