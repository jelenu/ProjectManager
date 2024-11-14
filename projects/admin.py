from django.contrib import admin
from .models import Project, ProjectStatus, PriorityLabel, ProjectUserRole

# Inline para gestionar la relación Many-to-Many
class ProjectUserRoleInline(admin.TabularInline):
    model = ProjectUserRole  # Modelo intermedio
    extra = 1  # Número de formularios vacíos que se mostrarán
    fields = ('user', 'role')  # Los campos que mostrarás para cada usuario asignado al proyecto

# Registrar el modelo ProjectStatus
@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Registrar el modelo PriorityLabel
@admin.register(PriorityLabel)
class PriorityLabelAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Registrar el modelo Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'status', 'priority', 'created_date', 'deadline_date', 'parent_project', 'display_users')
    search_fields = ('name', 'description', 'creator__username')
    list_filter = ('status', 'priority', 'parent_project')
    raw_id_fields = ('parent_project',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'creator', 'status', 'priority', 'deadline_date', 'parent_project')
        }),
    )
    inlines = [ProjectUserRoleInline]  # Añadir el InlineModelAdmin

    def display_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    display_users.short_description = 'Assigned Users'
