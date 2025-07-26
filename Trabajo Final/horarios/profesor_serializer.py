from rest_framework import serializers
from horarios.models import Professor, Availability, Course

# Serializador para disponibilidad horaria
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']

# Serializador para crear profesor
class ProfessorCreateSerializer(serializers.ModelSerializer):
    can_teach_courses = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Course.objects.all(), required=False
    )
    availabilities = AvailabilitySerializer(many=True, required=False)

    class Meta:
        model = Professor
        fields = [
            'first_name',
            'last_name',
            'academic_unit',
            'employment_type',
            'can_teach_courses',
            'availabilities'
        ]

    def validate(self, data):
        employment_type = data.get('employment_type')
        availabilities = data.get('availabilities', [])

        if employment_type == Professor.Employment.CONTRACT and not availabilities:
            raise serializers.ValidationError("Los docentes contratados deben tener disponibilidades.")
        if employment_type == Professor.Employment.FULL_TIME and availabilities:
            raise serializers.ValidationError("Los docentes nombrados no deben tener disponibilidades.")
        return data

    def create(self, validated_data):
        availabilities_data = validated_data.pop('availabilities', [])
        courses = validated_data.pop('can_teach_courses', [])
        professor = Professor.objects.create(**validated_data)

        if courses:
            professor.can_teach_courses.set(courses)

        for availability in availabilities_data:
            Availability.objects.create(professor=professor, **availability)

        return professor


class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code']

class ProfessorUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    can_teach_courses = CourseMiniSerializer(many=True, read_only=True)
    can_teach_courses_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Course.objects.all(), write_only=True, source='can_teach_courses'
    )

    availabilities = AvailabilitySerializer(many=True, required=False)
    
    class Meta:
        model = Professor
        fields = [
            'id',
            'first_name',
            'last_name',
            'academic_unit',
            'employment_type',
            'can_teach_courses',         # read-only con nombre del curso
            'can_teach_courses_ids',     # write-only para POST/PUT con IDs
            'availabilities'
        ]

    def validate(self, data):
        employment_type = data.get('employment_type')
        availabilities = data.get('availabilities', [])

        if employment_type == Professor.Employment.CONTRACT and not availabilities:
            raise serializers.ValidationError("Los docentes contratados deben tener disponibilidades.")
        if employment_type == Professor.Employment.FULL_TIME and availabilities:
            raise serializers.ValidationError("Los docentes nombrados no deben tener disponibilidades.")
        return data

    def update(self, instance, validated_data):
        availabilities_data = validated_data.pop('availabilities', [])
        courses = validated_data.pop('can_teach_courses', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar cursos
        if courses is not None:
            instance.can_teach_courses.set(courses)
            
        # Reemplazar disponibilidades
        instance.availabilities.all().delete()

        for availability in availabilities_data:
            Availability.objects.create(professor=instance, **availability)

        return instance

