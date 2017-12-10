##############################################
#      exceptions

class BaseError(Exception):
    message = "Running Error"

class ParameterError(BaseError):
    message = 'Parameter Error'

class ValidationError(BaseError):
    message = 'Validate Error'

class NotImplementationError(BaseError):
    message = 'Not Impleted'
