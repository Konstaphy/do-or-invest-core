from src import are_not_included, ValidationException


class GetEventsByDayRequest:
    date: None

    def __init__(self, request):
        if are_not_included(["date"], request):
            raise ValidationException
        self.date = request.get("date")
