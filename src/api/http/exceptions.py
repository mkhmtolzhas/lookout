from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized", status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str = "Internal Server Error", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)