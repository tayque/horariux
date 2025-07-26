
from django.db import models
from django.utils.translation import gettext_lazy as _

DAY = [(i, d) for i, d in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie"])]

class GlobalConstraint(models.Model):
    reason = models.CharField(max_length=120, verbose_name=_("Motivo"))
    day = models.PositiveSmallIntegerField(choices=DAY, verbose_name=_("Día"))
    start_time = models.TimeField(verbose_name=_("Inicio"))
    end_time = models.TimeField(verbose_name=_("Fin"))

    class Meta:
        verbose_name = _("Restricción global")
        verbose_name_plural = _("Restricciones globales")
        ordering = ("day", "start_time")

    def __str__(self):
        return f"{self.reason} – {self.get_day_display()} {self.start_time}-{self.end_time}"
