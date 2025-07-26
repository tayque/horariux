from django.contrib import admin
from horarios.models import (
    AcademicUnit, Professor, Availability,
    Curriculum, Term, AcademicYearLevel,
    Course, CourseGroup, Classroom,
    ScheduleVersion, Session, GlobalConstraint
)

@admin.register(AcademicUnit)
class AcademicUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("id", "get_full_name", "employment_type", "academic_unit")
    list_filter = ("employment_type", "academic_unit")
    search_fields = ("first_name", "last_name")

    @admin.display(description="Nombre completo")
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "professor", "day", "start_time", "end_time")
    list_filter = ("day", "professor")
    search_fields = ("professor__first_name", "professor__last_name")



@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("id", "year")
    list_filter = ("year",)
    search_fields = ("year",)


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "semester")
    list_filter = ("year", "semester")
    search_fields = ("year",)


@admin.register(AcademicYearLevel)
class AcademicYearLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "year_level", "semester_number")
    list_filter = ("year_level", "semester_number")
    search_fields = ("year_level",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "curriculum", "term", "academic_unit")
    list_filter = ("curriculum", "term", "academic_unit")
    search_fields = ("code", "name")


@admin.register(CourseGroup)
class CourseGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id", "course", "group_code", "shift",
        "capacity", "current_enrollment", "is_retake"
    )
    list_filter = ("shift", "is_retake", "course")
    search_fields = ("group_code",)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("id", "full_code", "short_code", "capacity", "is_lab", "year_preference")
    list_filter = ("is_lab",)
    search_fields = ("full_code", "short_code")


@admin.register(ScheduleVersion)
class ScheduleVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "term", "version_number", "state", "created_at")
    list_filter = ("state", "term")
    search_fields = ("version_number",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "course_group", "version", "day", "start_time",
        "duration_blocks", "classroom", "session_type", "professor"
    )
    list_filter = ("day", "session_type", "professor", "classroom")
    search_fields = ("course_group__group_code",)


@admin.register(GlobalConstraint)
class GlobalConstraintAdmin(admin.ModelAdmin):
    list_display = ("id", "reason", "day", "start_time", "end_time")
    list_filter = ("day",)
    search_fields = ("reason",)

