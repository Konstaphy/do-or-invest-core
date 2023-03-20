class ValidationException(Exception):
    message = None

    def __init__(self):
        self.message = "ValidationError"
