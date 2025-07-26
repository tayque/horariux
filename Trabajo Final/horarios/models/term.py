
from django.db import models
from django.utils.translation import gettext_lazy as _

class Term(models.Model):
    SEMESTER_CHOICES = [("A", _("A")), ("B", _("B"))]

    year = models.PositiveSmallIntegerField(verbose_name=_("Año"), db_index=True)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES,
                                verbose_name=_("Semestre"))

    class Meta:
        verbose_name = _("Período académico")
        verbose_name_plural = _("Períodos académicos")
        unique_together = ("year", "semester")
        ordering = ("-year", "-semester")

    def __str__(self):
        return f"{self.year}-{self.semester}"
