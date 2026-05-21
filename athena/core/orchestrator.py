import logging
from functools import lru_cache
from langgraph.graph import StateGraph, START, END
from openai import AsyncOpenAI

from athena.core.state import AthenaState
from athena.agents.learning_coach import LearningCoach
from athena.config.settings import get_settings

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        settings = get_settings()
        self.llm = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=30.0,
            max_retries=2
        )
        self.learning_coach = LearningCoach(self.llm)
        self.graph = self._build_graph()
        logger.info("✅ Orchestrator 初始化完成")

    def _build_graph(self):
        workflow = StateGraph(AthenaState)
        workflow.add_node("learning_coach", self.learning_coach.invoke)
        workflow.add_edge(START, "learning_coach")
        workflow.add_edge("learning_coach", END)
        return workflow.compile()

    async def run(self, user_input: str, user_id: str = "default",
                  session_id: str = "default") -> dict:
        initial_state = {
            "user_input": user_input,
            "user_id": user_id,
            "session_id": session_id,
            "messages": [],
            "reply": ""
        }
        logger.info(f"🚀 处理 [user={user_id}]: {user_input[:50]}")
        result = await self.graph.ainvoke(initial_state)
        return {"reply": result["reply"]}

@lru_cache
def get_orchestrator() -> Orchestrator:
    return Orchestrator()
