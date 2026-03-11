# pylint: disable=line-too-long, too-many-locals

from src.domain.use_cases.chat_ai import ChatAIInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import SuccessResponse
from src.presentation.interfaces.controller_interface import ControllerInterface


from src.logging_config import get_logger

logger = get_logger(__name__)


class SendMessageController(ControllerInterface):
    def __init__(
        self,
        chat_ai_use_case: ChatAIInterface
    ):
        self.__chat_ai_use_case = chat_ai_use_case

    async def handle(self, http_request: HttpRequest) -> SuccessResponse:

        try:
            body = http_request.body or {}
            message = body.get("content", "")
            ai_answer = await self.__chat_ai_use_case.send_message(message=message)

            return SuccessResponse(data=ai_answer)

        except Exception as e:
            raise e
