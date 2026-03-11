from fastapi import (
    APIRouter,
    Request,
    status,

)
from src.main.adapters.request_adapter import request_adapter
from src.main.composers.chat.send_message import send_message_composer

from src.presentation.http_types.http_response import SuccessResponse
from src.presentation.dtos.chat import SendMessageRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/messages",
    response_model=SuccessResponse[str],
    status_code=status.HTTP_201_CREATED,
    response_description="Send a new message to a chat",
    response_model_exclude_none=True
)
async def send_message(
    request: Request,
    body: SendMessageRequest
):
    """Send a new message to a chat session"""
    controller_handle = await send_message_composer()
    http_response = await request_adapter(
        request,
        controller_handle
    )
    return http_response
