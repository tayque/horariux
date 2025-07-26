
from django.db import models
from django.utils.translation import gettext_lazy as _

class AcademicYearLevel(models.Model):
    YEAR_CHOICES = [(i, _(f"{i}º año")) for i in range(1, 6)]
    SEM_CHOICES = [(1, _("1.er sem.")), (2, _("2.º sem."))]

    year_level = models.PositiveSmallIntegerField(choices=YEAR_CHOICES,
                                                  verbose_name=_("Año académico"))
    semester_number = models.PositiveSmallIntegerField(choices=SEM_CHOICES,
                                                       verbose_name=_("Semestre"))

    class Meta:
        verbose_name = _("Nivel académico")
        verbose_name_plural = _("Niveles académicos")
        unique_together = ("year_level", "semester_number")
        ordering = ("year_level", "semester_number")

    def __str__(self):
        return f"{self.get_year_level_display()} – {self.get_semester_number_display()}"
