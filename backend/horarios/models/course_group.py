
from django.db import models
from django.utils.translation import gettext_lazy as _

class CourseGroup(models.Model):
    SHIFT = [("M", _("Mañana")), ("T", _("Tarde")), ("A", _("Indistinto"))]

    course = models.ForeignKey("Course", related_name="groups",
                               on_delete=models.CASCADE, verbose_name=_("Curso"))
    group_code = models.CharField(max_length=2, verbose_name=_("Grupo"))  # A, B, C…
    shift = models.CharField(max_length=1, choices=SHIFT, verbose_name=_("Turno"))
    capacity = models.PositiveSmallIntegerField(default=40,
                                                verbose_name=_("Cupo máximo"))
    current_enrollment = models.PositiveSmallIntegerField(default=0,
                                                          verbose_name=_("Matrícula actual"))
    is_retake = models.BooleanField(default=False,
                                    verbose_name=_("Grupo de recuperación"))
    academic_year_level = models.ForeignKey("AcademicYearLevel",
                                            null=True, blank=True,
                                            on_delete=models.PROTECT,
                                            verbose_name=_("Nivel académico"))

    class Meta:
        verbose_name = _("Grupo de curso")
        verbose_name_plural = _("Grupos de curso")
        unique_together = ("course", "group_code")

    def __str__(self):
        return f"{self.course.code}-{self.group_code}"
