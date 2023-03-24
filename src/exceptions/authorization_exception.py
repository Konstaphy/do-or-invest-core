class AuthorizationException(Exception):
    message = "Unauthorized"

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
