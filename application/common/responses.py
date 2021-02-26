from domain.common.exceptions import InValidDomainException


class ResponseConverter:
    @staticmethod
    def convert_exception_to_response(exception: InValidDomainException) -> (dict, int):
        return {"message": exception.message}, 400
