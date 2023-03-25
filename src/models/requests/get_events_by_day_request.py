from src.exceptions.validation_exception import ValidationException
from src.utils.are_not_included import are_not_included


class GetEventsByDayRequest:
    date: None

    def __init__(self, request):
        if are_not_included(["date"], request):
            raise ValidationException
        self.date = request.get("date")
