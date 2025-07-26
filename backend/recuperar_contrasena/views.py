# en views.py
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny]) 
def recuperacion(request):
    email_list = ["rcamargoh@unsa.edu.pe", "pmaytaqu@unsa.edu.pe"]
    reason = request.data.get('reason')

    if not email_list or not reason:
        return Response({"error": "Faltan datos"}, status=400)

    send_mail(
        'Solicitud de recuperación de contraseña por parte de usuario',
        f'Se ha recibido una solicitud de recuperación de contraseña. \n Motivo: {reason}',
        'tucorreo@gmail.com',
        email_list,
        fail_silently=False,
    )

    return Response({"message": "Correo enviado correctamente."}, status=200)
