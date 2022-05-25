class CustomException(Exception):
    message: str

    def __init__(self, message):
        self.message = message


class KeyError(CustomException):
    pass


class ValueError(CustomException):
    pass


class FileReadingError(CustomException):
    pass


class CopyError(CustomException):
    pass
