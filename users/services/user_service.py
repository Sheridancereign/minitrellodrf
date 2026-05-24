from django.contrib.auth import get_user_model


def create_user(*, username, last_name, email, password):
    User = get_user_model()

    return User.objects.create_user(
        username=username,
        last_name=last_name,
        email=email,
        password=password,
    )
