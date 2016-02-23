class BadRequestException(Exception):

    def __init__(self, message):
        super(BadRequestException, self).__init__(message)
