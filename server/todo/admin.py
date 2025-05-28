from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Task, User, TechParkParticipants


class ToDoListAdminSite(admin.AdminSite):
    pass


todo_list_admin_site = ToDoListAdminSite(name="todo_list_admin")


@admin.register(User, site=todo_list_admin_site)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    ordering = ("email",)


@admin.register(Task, site=todo_list_admin_site)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("updated_at",)
    list_display = ("__str__", "completed", "updated_at")
    ordering = ("id",)


@admin.register(TechParkParticipants, site=todo_list_admin_site)
class TechParkParticipantsAdmin(admin.ModelAdmin):
    ordering = ("serial_number",)
    list_display = (
        "serial_number",
        "join_date",
        "end_date",
        "bin",
        "display_status",
        "company_name",
    )

    @admin.display(boolean=True, description="Status")
    def display_status(self, obj):
        return obj.status
