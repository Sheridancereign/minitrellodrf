from boards.models import BoardMembership


def get_membership(*, user, board):
    return BoardMembership.objects.filter(
        user=user,
        board=board,
    ).first()


def can_assign_task(*, user, board):
    if user.is_superuser:
        return True

    membership = get_membership(
        user=user,
        board=board,
    )

    if not membership:
        return False

    return membership.role in (
        BoardMembership.Role.OWNER,
        BoardMembership.Role.MANAGER,
    )
