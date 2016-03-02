class OpenpuckException(Exception):
    """
    Template class for all exceptions.
    """
    def __init__(self, message):
        super(OpenpuckException, self).__init__(self.__class__.__name__ + ": " + message)

class BadRequestException(OpenpuckException):
    """
    400 Bad Request
    """
    def __init__(self, message):
        super(BadRequestException, self).__init__(message)

class NotFoundException(OpenpuckException):
    """
    404 Not Found
    """
    def __init__(self, message):
        super(NotFoundException, self).__init__(message)
