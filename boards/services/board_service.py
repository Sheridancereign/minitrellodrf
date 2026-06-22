from boards.models import BoardMembership
from boards.services import permission_service


def assign_board_member(*, board, user, actor):
    if not permission_service.can_manage_board_members(user=actor):
        raise ValueError("You do not have permission to manage board members")

    membership, _ = BoardMembership.objects.get_or_create(
        board=board,
        user=user,
    )

    return membership
