from src.exceptions.validation_exception import ValidationException
from src.utils.are_not_included import are_not_included


class NewDataRequest:
    description = None
    priority = None

    def __init__(self, json_request):
        if are_not_included(["description", "priority"], json_request):
            raise ValidationException()

        self.description = json_request.get("description")
        self.priority = json_request.get("priority")
