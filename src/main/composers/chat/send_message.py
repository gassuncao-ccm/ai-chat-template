from typing import Any, List
from langchain_openai import ChatOpenAI

from src.infrastructure.ai.strategies.langgraph_strategy import LangGraphStrategy
from src.infrastructure.ai.langgraph_services.graphs.default_graph import CRMGraph
from src.infrastructure.ai.langgraph_services.callbacks.custom_callback_handler import (
    CustomCallbackHandler,
)

from src.application.use_cases.chat_ai import ChatAI
from src.infrastructure.config.settings import settings
from src.presentation.controllers.chat.send_message import SendMessageController

def _build_graph(
    llm: ChatOpenAI,
    crm_agents: List[Any],

) -> CRMGraph:
    return CRMGraph(
        llm=llm,
        agents=crm_agents,
    )

async def send_message_composer():

    llm = ChatOpenAI(
        model=settings.CONVERSATION_MODEL,
        temperature=0,
        max_retries=5
    )

    graph_builder = _build_graph(
        llm=llm,
        crm_agents=[], # insert your agents for the supervisor to delegate tasks
    )

    ai_strategy = LangGraphStrategy(
        graph_builder=graph_builder,
        callback=CustomCallbackHandler(),
    )
    use_case = ChatAI(ai_strategy)

    controller = SendMessageController(use_case)
    return controller.handle
