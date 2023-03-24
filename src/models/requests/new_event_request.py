from src import ValidationException, are_not_included


class NewEventRequest:
    title = None
    date = None
    time = None
    priority = None
    user_id = None

    def __init__(self, json_request):
        if are_not_included(["title", "date", "time", "user_id", "priority"], json_request):
            raise ValidationException()

        self.title = json_request.get("title")
        self.date = json_request.get("date")
        self.time = json_request.get("time")
        self.priority = json_request.get("priority")
        self.user_id = json_request.get("user_id")
