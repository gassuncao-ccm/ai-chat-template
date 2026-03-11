# pylint: disable=line-too-long, too-many-arguments, too-many-positional-arguments, too-many-locals
from langchain_core.callbacks.base import BaseCallbackHandler


from src.domain.strategies.ai_strategy import AIStrategyInterface
from src.infrastructure.ai.langgraph_services.interfaces.graph_builder import GraphBuilderInterface

from src.logging_config import get_logger

logger = get_logger(__name__)

class LangGraphStrategy(AIStrategyInterface):

    def __init__(
        self,
        graph_builder: GraphBuilderInterface,
        callback: BaseCallbackHandler
    ):
        self.graph = graph_builder.create_graph()
        self.callback = callback

    async def generate_response(
        self,
        message: str
    ) -> str:
        """Generate a complete AI response (non-streaming).

        This method can return either a plain string message or a tool_call response dict.
        Tool calls require human approval before proceeding.

        Args:
            message: The user message to generate a response for.

        Returns:
            str: The generated AI response message.
        """
        logger.info(
            "Generating AI response",
            extra={"event": "generate_response_complete_start"}
        )

        input_state = {
            "messages": message,
        }

        result = await self.graph.ainvoke(input_state, version="v2")
        messages = result.value.get("messages", [])

        return messages[-1].content