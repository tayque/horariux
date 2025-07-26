# schedule_serializer.py
from rest_framework import serializers

class HorarioGeneradoInputSerializer(serializers.Serializer):
    term_id = serializers.ChoiceField(choices=['1', '2'])
    mallas_por_año = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Diccionario con año académico como clave y año de malla como valor"
    )
    cursos_c = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="IDs de cursos con sección C"
    )
