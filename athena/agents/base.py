"""所有 Agent 的基类，强制统一接口"""

from abc import ABC, abstractmethod
from openai import AsyncOpenAI


class BaseAgent(ABC):
    """
    Agent 基类

    设计原则：
    1. 所有 Agent 必须实现 invoke 方法
    2. invoke 接收 state（dict），返回 state 的更新字段（dict）
    3. LLM 客户端通过依赖注入传入，方便测试
    """

    def __init__(self, llm_client: AsyncOpenAI, name: str = "BaseAgent"):
        self.llm = llm_client
        self.name = name

    @abstractmethod
    async def invoke(self, state: dict) -> dict:
        """每个 Agent 必须实现的执行方法"""
        pass