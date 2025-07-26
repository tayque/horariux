# models/professor.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from .academic_unit import AcademicUnit
from .course import Course

class Professor(models.Model):
    class Employment(models.TextChoices):
        FULL_TIME = "FT", _("Tiempo completo")
        CONTRACT = "CT", _("Contratado")

    first_name = models.CharField(max_length=60, verbose_name=_("Nombres"))
    last_name = models.CharField(max_length=60, verbose_name=_("Apellidos"))
    academic_unit = models.ForeignKey(AcademicUnit, on_delete=models.SET_NULL, null=True)
    employment_type = models.CharField(max_length=2, choices=Employment.choices, default=Employment.FULL_TIME)
    can_teach_courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
