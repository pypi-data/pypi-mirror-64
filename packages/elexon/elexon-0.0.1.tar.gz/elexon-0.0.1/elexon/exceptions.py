class ElexonException(Exception):
    """The base Elexon Exception that all other exception classes extend."""
    pass

class Unavailable(ElexonException):
    pass

class PaymentGatewayError(ElexonException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class Refused(PaymentGatewayError):
    pass

class Stolen(PaymentGatewayError):
    pass
