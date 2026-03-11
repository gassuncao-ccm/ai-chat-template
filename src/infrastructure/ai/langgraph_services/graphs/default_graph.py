from typing import List, Optional


from langgraph.typing import ContextT, InputT, OutputT, StateT
from langgraph.graph.state import CompiledStateGraph
from langgraph_supervisor import create_supervisor

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLanguageModel
from src.infrastructure.ai.langgraph_services.interfaces.graph_builder import GraphBuilderInterface

class CRMGraph(GraphBuilderInterface):
    def __init__(
        self,
        llm: BaseLanguageModel,
        agents: List[CompiledStateGraph],
        handoff_tools: Optional[List[BaseTool]] = None,
        pre_model_hook: Optional[callable] = None,
        supervisor_prompt: Optional[str] = "You are a supervisor, answer the questions"
    ):
        self.__llm = llm
        self.__agents = agents
        self.__handoff_tools = handoff_tools
        self.__pre_model_hook = pre_model_hook
        self.__supervisor_prompt = supervisor_prompt

    def create_graph(self) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]:
        erp_assistant_workflow = create_supervisor(
            agents=self.__agents,
            model=self.__llm,
            tools=self.__handoff_tools or None,
            output_mode="last_message",
            prompt=self.__supervisor_prompt,
            pre_model_hook=self.__pre_model_hook,
        )

        return erp_assistant_workflow.compile()
