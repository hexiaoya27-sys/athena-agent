from abc import ABC, abstractmethod
from openai import AsyncOpenAI

class BaseAgent(ABC):
    def __init__(self, llm_client: AsyncOpenAI, name: str = "BaseAgent"):
        self.llm = llm_client
        self.name = name

    @abstractmethod
    async def invoke(self, state: dict) -> dict:
        pass
