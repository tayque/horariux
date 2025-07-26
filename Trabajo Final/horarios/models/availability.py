# models/availability.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from .professor import Professor

class Availability(models.Model):
    professor = models.ForeignKey(Professor, related_name='availabilities', on_delete=models.CASCADE)
    
    class Days(models.TextChoices):
        MON = "Lunes", _("Lunes")
        TUE = "Martes", _("Martes")
        WED = "Miércoles", _("Miércoles")
        THU = "Jueves", _("Jueves")
        FRI = "Viernes", _("Viernes")

    day = models.CharField(max_length=20, choices=Days.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
