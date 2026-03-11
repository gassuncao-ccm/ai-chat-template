from abc import ABC, abstractmethod

class AIStrategyInterface(ABC):

    @abstractmethod
    async def generate_response(
        self,
        message: str,
    ) -> str: pass
