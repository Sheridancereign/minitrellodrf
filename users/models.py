from functools import cached_property

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.permissions import PermissionGroups


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    @cached_property
    def is_super_admin(self):
        return (
            self.is_superuser
            or self.groups.filter(name=PermissionGroups.SUPER_ADMIN).exists()
        )

    @cached_property
    def is_manager(self):
        return self.groups.filter(name=PermissionGroups.MANAGER).exists()

    @cached_property
    def is_member(self):
        return self.groups.filter(name=PermissionGroups.MEMBER).exists()
