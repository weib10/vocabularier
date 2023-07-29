class OutOfRangeExecption(Exception):
    """My own exception class

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class InvalidInputExecption(Exception):
    """My own exception class

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
