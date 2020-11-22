class ApiException(Exception):
    pass


class KeyExistsException(ApiException):
    message = "Key already exists"
    code = 409


class KeyNotExistsException(ApiException):
    message = "Key doesn't exists"
    code = 404
