
from django.db import models
from django.utils.translation import gettext_lazy as _

class AcademicUnit(models.Model):
    code = models.CharField(max_length=20, unique=True,
                            verbose_name=_("Código depeartamente"))

    name = models.CharField(max_length=120, verbose_name=_("Nombre departamento"))

    class Meta:
        verbose_name = _("Departamento académico")
        verbose_name_plural = _("Deparatamentos académicos")
        ordering = ("code",)

    def __str__(self):
        return f"{self.code} – {self.name}"
