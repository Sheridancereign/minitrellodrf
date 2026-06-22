from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from users.permissions import PermissionGroups

ROLE_PERMISSIONS = {
    PermissionGroups.SUPER_ADMIN: [
        "add_board",
        "view_board",
        "change_board",
        "delete_board",
        "manage_board_members",
        "add_task",
        "view_task",
        "change_task",
        "delete_task",
        "assign_task",
        "view_taskactivity",
    ],
    PermissionGroups.MANAGER: [
        "add_board",
        "view_board",
        "change_board",
        "manage_board_members",
        "add_task",
        "view_task",
        "change_task",
        "assign_task",
        "view_taskactivity",
    ],
    PermissionGroups.MEMBER: [
        "view_board",
        "add_task",
        "view_task",
        "change_task",
        "view_taskactivity",
    ],
}


class Command(BaseCommand):
    help = "Create system roles and assign permissions"

    def handle(self, *args, **options):
        for group_name, codenames in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)

            permissions = Permission.objects.filter(
                content_type__app_label="boards",
                codename__in=codenames,
            )

            group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Roles configured"))
