from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    ...


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    ...


task_manager_admin_site.register(User, UserAdmin)
