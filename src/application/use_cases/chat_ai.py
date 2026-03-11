from src.domain.use_cases.chat_ai import ChatAIInterface
from src.domain.strategies.ai_strategy import AIStrategyInterface

from src.logging_config import get_logger

logger = get_logger(__name__)

class ChatAI(ChatAIInterface):
    """Service layer handling chat persistence, retrieval, and AI strategy interaction."""

    def __init__(
        self,
        ai_strategy: AIStrategyInterface
    ):
        self.__ai_strategy = ai_strategy

    async def send_message(
        self,
        message: str
    ) -> dict:
        """Get a complete AI response (non-streaming).

        Args:
            message: User message
        Returns:
            Dict with AI message data.
        """

        logger.info(
            "Generating complete AI response for user message",
            extra={
                "event": "send_message_start",
            }
        )
        try:
            generated_ai_message = await self.__ai_strategy.generate_response(message)
            return generated_ai_message
        except Exception as e:
            logger.error(
                "Unexpected error getting AI response",
                extra={"event": "ai_response_error", "error": str(e)},
                exc_info=True
            )
            raise e
