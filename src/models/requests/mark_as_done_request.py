from src import ValidationException


class MarkAsDoneRequest:
    event_id = None

    def __init__(self, request):
        if request.get("event_id") is None:
            raise ValidationException()
        self.event_id = request.get("event_id")
