from abc import ABC, abstractmethod

class ChatAIInterface(ABC):
    """Service layer handling chat persistence, retrieval, and AI strategy interaction."""

    @abstractmethod
    async def send_message(
        self,
        message: str
    ) -> str: pass
