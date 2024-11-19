# Importing necessary modules from Django REST Framework and the models
from rest_framework import serializers
from .models import Project, ProjectStatus, PriorityLabel, ProjectUserRole

# Serializer for the Project model
class ProjectSerializer(serializers.ModelSerializer):
    # Defining a relationship field for parent_project, which is optional (required=False)
    parent_project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False) 
    # Defining a relationship field for the project status
    status = serializers.PrimaryKeyRelatedField(queryset=ProjectStatus.objects.all())
    # Defining a relationship field for the project's priority label
    priority = serializers.PrimaryKeyRelatedField(queryset=PriorityLabel.objects.all())

    class Meta:
        # The model this serializer corresponds to is 'Project'
        model = Project
        # Specifying which fields will be included in the serialized data
        fields = ['name', 'description', 'deadline_date', 'status', 'priority', 'parent_project']

    def create(self, validated_data):
        # Getting the current user from the request context, who will be the creator of the project
        creator = self.context['request'].user
        # Creating a new project instance with the validated data and the creator user
        project = Project.objects.create(creator=creator, **validated_data)

        # Automatically creating a 'ProjectUserRole' record to assign the creator as an 'admin' in the new project
        ProjectUserRole.objects.create(
            project=project,
            user=creator,
            role='admin'
        )
        
        # Returning the newly created project instance
        return project


# Serializer for the ProjectStatus model
class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        # The model this serializer corresponds to is 'ProjectStatus'
        model = ProjectStatus
        # Specifying the fields that will be included in the serialized data
        fields = ['id', 'name']


# Serializer for the PriorityLabel model
class PriorityLabelSerializer(serializers.ModelSerializer):
    class Meta:
        # The model this serializer corresponds to is 'PriorityLabel'
        model = PriorityLabel
        # Specifying the fields that will be included in the serialized data
        fields = ['id', 'name']
