"""学习教练 Agent - 第一周的 MVP Agent"""

import logging
from athena.agents.base import BaseAgent
from athena.config.settings import get_settings

logger = logging.getLogger(__name__)

LEARNING_COACH_PROMPT = """你是 Athena 系统的学习教练，名叫"雅典娜"。

你的特点：
- 温暖、耐心、善于启发
- 擅长用苏格拉底式提问引导用户思考
- 回答简洁，避免长篇大论（控制在 200 字内）
- 始终用中文回答

如果用户只是打招呼，请热情回应并主动询问他们今天想学什么。"""


class LearningCoach(BaseAgent):
    """学习教练 Agent"""

    def __init__(self, llm_client):
        super().__init__(llm_client, name="LearningCoach")

    async def invoke(self, state: dict) -> dict:
        settings = get_settings()
        user_input = state["user_input"]

        logger.info(f"[{self.name}] 处理输入: {user_input[:50]}...")

        try:
            response = await self.llm.chat.completions.create(
                model=settings.llm_main_model,
                messages=[
                    {"role": "system", "content": LEARNING_COACH_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=500,
                timeout=30.0
            )
            reply = response.choices[0].message.content
            logger.info(f"[{self.name}] 回复生成成功")
            return {"reply": reply}

        except Exception as e:
            logger.error(f"[{self.name}] LLM 调用失败: {e}")
            return {"reply": f"抱歉，我现在有点忙不过来（{type(e).__name__}）。请稍后再试。"}