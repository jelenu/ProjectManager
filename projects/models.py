from django.db import models
from authentication.models import CustomUser

class ProjectStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PriorityLabel(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    created_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(PriorityLabel, on_delete=models.SET_NULL, null=True)

    parent_project = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sub_projects'
    )

    # Many-to-many relationship for users assigned to the project
    users = models.ManyToManyField(CustomUser, through='ProjectUserRole', related_name='projects')

    def __str__(self):
        return self.name

class ProjectUserRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('collaborator', 'Collaborator'),
        ('observer', 'Observer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.project.name}"
