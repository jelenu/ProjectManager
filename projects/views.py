from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProjectStatus, PriorityLabel
from .serializers import ProjectSerializer, ProjectStatusSerializer, PriorityLabelSerializer
class CreateProjectAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):

        
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                'message': 'Proyecto creado con éxito',
                'project': ProjectSerializer(project, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusPriorityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener todas las instancias de ProjectStatus y PriorityLabel
        project_statuses = ProjectStatus.objects.all()
        priority_labels = PriorityLabel.objects.all()

        # Serializar ambos conjuntos de datos
        project_status_serializer = ProjectStatusSerializer(project_statuses, many=True)
        priority_label_serializer = PriorityLabelSerializer(priority_labels, many=True)

        # Devolver ambos en un solo diccionario dentro de la respuesta
        return Response({
            'project_statuses': project_status_serializer.data,
            'priority_labels': priority_label_serializer.data
        })