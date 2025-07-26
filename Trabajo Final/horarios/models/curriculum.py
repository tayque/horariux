
from django.db import models
from django.utils.translation import gettext_lazy as _

class Curriculum(models.Model):
    year = models.PositiveSmallIntegerField(unique=True,
                                            verbose_name=_("Año de malla"))

    class Meta:
        verbose_name = _("Malla curricular")
        verbose_name_plural = _("Mallas curriculares")
        ordering = ("-year",)

    def __str__(self):
        return str(self.year)
