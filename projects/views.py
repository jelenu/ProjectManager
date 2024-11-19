# Importing necessary modules from Django REST Framework and the models/serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProjectStatus, PriorityLabel
from .serializers import ProjectSerializer, ProjectStatusSerializer, PriorityLabelSerializer

# View to handle project creation (POST request)
class CreateProjectAPIView(APIView):
    # Restrict access to authenticated users only
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        # Initialize the ProjectSerializer with the incoming request data and context (for user access)
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        
        # Check if the serializer is valid (i.e., the incoming data is correct)
        if serializer.is_valid():
            # Save the project and return the response with the project details
            project = serializer.save()
            return Response({
                'message': 'Proyecto creado con éxito',  # Success message in Spanish
                'project': ProjectSerializer(project, context={'request': request}).data  # Serialized project data
            }, status=status.HTTP_201_CREATED)  # HTTP status for successful creation
        
        # If the serializer is not valid, return the error messages with HTTP 400 status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to handle fetching project statuses and priority labels (GET request)
class StatusPriorityAPIView(APIView):
    # Restrict access to authenticated users only
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all project statuses and priority labels from the database
        project_statuses = ProjectStatus.objects.all()
        priority_labels = PriorityLabel.objects.all()

        # Serialize the project statuses and priority labels
        project_status_serializer = ProjectStatusSerializer(project_statuses, many=True)
        priority_label_serializer = PriorityLabelSerializer(priority_labels, many=True)

        # Return the serialized data as the response
        return Response({
            'project_statuses': project_status_serializer.data,  # Serialized project statuses
            'priority_labels': priority_label_serializer.data  # Serialized priority labels
        })
