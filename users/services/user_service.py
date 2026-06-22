from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.permissions import PermissionGroups


def create_user(*, username, last_name, email, password):
    User = get_user_model()

    user = User.objects.create_user(
        username=username,
        last_name=last_name,
        email=email,
        password=password,
    )

    member_group, _ = Group.objects.get_or_create(name=PermissionGroups.MEMBER)
    user.groups.add(member_group)

    return user
