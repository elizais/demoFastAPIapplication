class BasetServiceError(Exception):
    pass


class ClientError(BasetServiceError):
    pass


class ServerError(BasetServiceError):
    pass


class EntityConflictError(ClientError):
    pass


class EntityDoesNotExistError(ClientError):
    pass
