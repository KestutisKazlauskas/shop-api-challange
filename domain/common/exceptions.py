class InValidDomainException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message


class InvalidPriceComparisonException(InValidDomainException):
    pass
