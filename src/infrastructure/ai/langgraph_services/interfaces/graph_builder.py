from abc import ABC, abstractmethod
from langgraph.graph.state import CompiledStateGraph

class GraphBuilderInterface(ABC):

    @abstractmethod
    def create_graph(self) -> CompiledStateGraph:
        """Compiles and returns the StateGraph."""
