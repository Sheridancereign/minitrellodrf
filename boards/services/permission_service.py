def can_manage_board_members(*, user):
    return user.is_superuser or user.has_perm("boards.manage_board_members")


def can_assign_task(*, user):
    return user.is_superuser or user.has_perm("boards.assign_task")


def can_create_board(*, user):
    return user.is_superuser or user.has_perm("boards.add_board")


def can_view_board(*, user):
    return user.is_superuser or user.has_perm("boards.view_board")


def can_create_task(*, user):
    return user.is_superuser or user.has_perm("boards.add_task")


def can_change_task(*, user):
    return user.is_superuser or user.has_perm("boards.change_task")
