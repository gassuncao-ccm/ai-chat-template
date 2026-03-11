from typing import Callable, Dict, Any, Optional
from fastapi import Request as FastAPIRequest
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import SuccessResponse

async def request_adapter(
    request: FastAPIRequest,
    controller: Callable,
    form_data: Optional[Dict[str, Any]] = None,
    path_params: Optional[Dict[str, Any]] = None
) -> SuccessResponse:

    body = None
    try:
        body = await request.json()
    except Exception:
        pass

    http_request = HttpRequest(
        body=body,
        header=dict(request.headers),
        query_params=dict(request.query_params),
        path_params=path_params or {},
        url=str(request.url),
        form_data=form_data
    )

    http_response = await controller(http_request)
    return http_response
