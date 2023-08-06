

class FieldRequired(Exception):
    def __init__(self, field, errors):
        # Call the base class constructor with the parameters it needs
        message = "The field {} is required".format(field)
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors


class FieldError(Exception):
    def __init__(self, field, errors):
        # Call the base class constructor with the parameters it needs
        message = "The field {} is wrong".format(field)
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors
