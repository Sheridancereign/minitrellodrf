from rest_framework.exceptions import APIException


class TaskDomainException(APIException):
    status_code = 400
    default_detail = "Task domain error"