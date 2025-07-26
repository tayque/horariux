
from django.db import models
from django.utils.translation import gettext_lazy as _

class ScheduleVersion(models.Model):
    STATE = [("draft", _("Borrador")), ("review", _("En revisión")),
             ("approved", _("Aprobado")), ("final", _("Final"))]

    term = models.ForeignKey("Term", on_delete=models.CASCADE,
                             verbose_name=_("Período académico"))
    version_number = models.PositiveSmallIntegerField(default=1,
                                                      verbose_name=_("Número de versión"))
    created_by = models.CharField(max_length=120, verbose_name=_("Creado por"))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Fecha creación"))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_("Última actualización"))
    state = models.CharField(max_length=10, choices=STATE, default="draft",
                             verbose_name=_("Estado"))
    notes = models.TextField(blank=True, verbose_name=_("Observaciones"))

    class Meta:
        verbose_name = _("Versión de horario")
        verbose_name_plural = _("Versiones de horario")
        unique_together = ("term", "version_number")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.term} v{self.version_number} – {self.get_state_display()}"
