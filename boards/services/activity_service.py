from boards.models import TaskActivity

class ActivityService:
    @staticmethod
    def log_task_created(*, task, actor):

        TaskActivity.objects.create(
            task=task,
            actor=actor,
            action=TaskActivity.Action.CREATED
        )
    @staticmethod
    def log_field_change(
        *,
        task,
        actor,
        field,
        old_value,
        new_value,
        action,
    ):
        TaskActivity.objects.create(
            task=task,
            actor=actor,
            field=field,
            old_value=str(old_value),
            new_value=str(new_value),
            action=action,
        )