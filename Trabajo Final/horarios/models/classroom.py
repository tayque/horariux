
from django.db import models
from django.utils.translation import gettext_lazy as _

class Classroom(models.Model):
    full_code = models.CharField(max_length=20, unique=True,
                                 verbose_name=_("Código completo"))
    short_code = models.CharField(max_length=10,
                                  verbose_name=_("Código corto"))
    capacity = models.PositiveIntegerField(verbose_name=_("Capacidad"))
    is_lab = models.BooleanField(default=False, verbose_name=_("¿Laboratorio?"))
    year_preference = models.PositiveSmallIntegerField(null=True, blank=True,
                                                       verbose_name=_("Año preferente"))

    class Meta:
        verbose_name = _("Aula")
        verbose_name_plural = _("Aulas")
        ordering = ("full_code",)

    def __str__(self):
        return self.full_code
