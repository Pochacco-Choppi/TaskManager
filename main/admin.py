from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    ...


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "author_link", "assignee_link", "deadline_date", "status")

    def author_link(self, obj):
        url = reverse("admin:main_user_change", args=[obj.author.id])
        link = '<a href="%s">%s</a>' % (url, obj.author.username)
        return mark_safe(link)

    author_link.short_description = "Author"

    def assignee_link(self, obj):
        url = reverse("admin:main_user_change", args=[obj.assignee.id])
        link = '<a href="%s">%s</a>' % (url, obj.assignee.username)
        return mark_safe(link)

    assignee_link.short_description = "Assignee"


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(User, site=task_manager_admin_site)
class CustomUserAdmin(UserAdmin):
    UserAdmin.list_display += ("role",)
    UserAdmin.fieldsets += (("Role", {"fields": ("role",)}),)
