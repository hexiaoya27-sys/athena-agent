"""LangGraph 主编排器 - 第一周只串一个 Agent，后续会扩展为多 Agent"""

import logging
from functools import lru_cache
from langgraph.graph import StateGraph, START, END
from openai import AsyncOpenAI

from athena.core.state import AthenaState
from athena.agents.learning_coach import LearningCoach
from athena.config.settings import get_settings

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    LangGraph 多 Agent 编排器

    第一周架构（最简）：
        START → LearningCoach → END

    第 3-4 周会演进为：
        START → IntentClassifier → Router → [多个 Agent] → Monitor → END
    """

    def __init__(self):
        settings = get_settings()

        # 初始化 LLM 客户端（生产级配置）
        self.llm = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=30.0,
            max_retries=2
        )

        # 初始化所有 Agent
        self.learning_coach = LearningCoach(self.llm)

        # 构建 LangGraph
        self.graph = self._build_graph()
        logger.info("✅ Orchestrator 初始化完成")

    def _build_graph(self):
        """构建 LangGraph 工作流"""
        workflow = StateGraph(AthenaState)

        # 添加节点
        workflow.add_node("learning_coach", self.learning_coach.invoke)

        # 定义边
        workflow.add_edge(START, "learning_coach")
        workflow.add_edge("learning_coach", END)

        return workflow.compile()

    async def run(self, user_input: str, user_id: str = "default",
                  session_id: str = "default") -> dict:
        """运行一次完整对话"""
        initial_state = {
            "user_input": user_input,
            "user_id": user_id,
            "session_id": session_id,
            "messages": [],
            "reply": ""
        }

        logger.info(f"🚀 开始处理 [user={user_id}]: {user_input[:50]}...")
        result = await self.graph.ainvoke(initial_state)
        logger.info(f"✅ 处理完成 [user={user_id}]")

        return {"reply": result["reply"]}


@lru_cache
def get_orchestrator() -> Orchestrator:
    """单例模式（FastAPI 启动时只初始化一次）"""
    return Orchestrator()