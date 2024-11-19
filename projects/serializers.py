from rest_framework import serializers
from authentication.models import CustomUser
from .models import Project, ProjectUserRole, ProjectStatus, PriorityLabel


class ProjectUserRoleSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # Identificar usuario por su `username`
    role = serializers.ChoiceField(choices=ProjectUserRole.ROLE_CHOICES)

    class Meta:
        model = ProjectUserRole
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    users = ProjectUserRoleSerializer(many=True, required=False)  # Usuarios y roles asociados al proyecto
    parent_project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)  # Proyecto padre opcional
    status = serializers.PrimaryKeyRelatedField(queryset=ProjectStatus.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=PriorityLabel.objects.all())

    class Meta:
        model = Project
        fields = ['name', 'description', 'deadline_date', 'status', 'priority', 'parent_project', 'users']

    def create(self, validated_data):
        # Extraer datos de usuarios relacionados
        users_data = validated_data.pop('users', [])
        
        # Crear el proyecto
        project = Project.objects.create(creator=self.context['request'].user, **validated_data)

        # Asociar usuarios y roles al proyecto
        for user_data in users_data:
            try:
                user = CustomUser.objects.get(username=user_data['user'])
                ProjectUserRole.objects.create(
                    project=project,
                    user=user,
                    role=user_data['role']
                )
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"user": f"User {user_data['user']} not found."})

        return project


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ['id', 'name']

class PriorityLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityLabel
        fields = ['id', 'name']