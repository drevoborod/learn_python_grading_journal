from fastapi import HTTPException, status


class HTTPError(HTTPException): pass


class DataNotFoundError(HTTPError):
    def __init__(self, detail: str | None = None):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)