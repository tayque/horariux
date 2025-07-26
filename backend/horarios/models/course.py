# models/course.py

from django.db import models
from .academic_unit import AcademicUnit
from .term import Term
from .curriculum import Curriculum
from .academic_year_level import AcademicYearLevel

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    academic_unit = models.ForeignKey(AcademicUnit, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    course_credits = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)
    ht = models.IntegerField(default=0)
    htp = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    hs = models.IntegerField(default=0)
    hl = models.IntegerField(default=0)
    comp = models.CharField(max_length=2, default="N", choices=[
        ("N", "Ninguno"),
        ("A", "Formación Básica"), 
        ("B", "Formación Especializada"), 
        ("C", "Formación Profesional y Otros"), 
        ("D", "Est.Gen.: Capacidades de Aprendizaje"),
        ("E", "Est.Gen.: Form.Humanist.Ident. y Ciudadanía"), 
        ("F", "Estudios Específicos"), 
        ("G", "Estudios de Especialidad"),
    ])
    academic_year_level = models.ForeignKey(AcademicYearLevel,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name
