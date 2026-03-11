from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.presentation.http_types.http_response import ErrorResponse

from src.logging_config import get_logger

logger = get_logger(__name__)


HTTP_STATUS_MAP = {
    #ChatNotFoundError: status.HTTP_404_NOT_FOUND,
}


def get_http_status(exception: Exception) -> int:
    """Map exception to HTTP status code."""
    for exc_class, status_code in HTTP_STATUS_MAP.items():
        if isinstance(exception, exc_class):
            return status_code
    return status.HTTP_500_INTERNAL_SERVER_ERROR


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error("Error on request: %s", str(e), exc_info=True)

            http_status = get_http_status(e)

            message = str(e)
            response = JSONResponse(
                status_code=http_status,
                content=ErrorResponse(
                    message=message,
                ).model_dump()
            )

            origin = request.headers.get("origin", "*")
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"

            return response
