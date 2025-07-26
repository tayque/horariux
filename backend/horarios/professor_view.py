from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from horarios.models import Professor
from horarios.profesor_serializer import ProfessorUpdateSerializer
from rest_framework.permissions import AllowAny  # 👈 Asegúrate de importar esto

from .profesor_serializer import ProfessorCreateSerializer

class ProfessorCreateView(APIView):
    permission_classes = [AllowAny]  # 👈 Esto permite acceso sin autenticación

    def post(self, request):
        serializer = ProfessorCreateSerializer(data=request.data)
        if serializer.is_valid():
            professor = serializer.save()
            return Response({'message': 'Profesor creado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfessorUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorUpdateSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'
class ProfessorListView(ListAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorUpdateSerializer
    permission_classes = [AllowAny]