from typing import Literal
from pydantic import BaseModel, Field


# ⭐ 关键：用 Pydantic 定义结构化输出 Schema
class IntentResult(BaseModel):
    primary_intent: Literal[
        "learning", "fitness", "psychology",
        "goal_management", "casual_chat", "tool_use", "unclear"
    ] = Field(description="主意图")

    sub_intent: str = Field(description="子意图，如'概念解释'、'计划制定'")

    emotion: Literal["calm", "anxious", "excited", "frustrated", "sad", "neutral"] = Field(
        description="用户情绪状态"
    )

    urgency: Literal["low", "medium", "high", "critical"] = Field(
        description="紧迫程度"
    )

    confidence: float = Field(ge=0, le=1, description="意图识别置信度")

    needs_clarification: bool = Field(description="是否需要反问澄清")
    clarification_question: str = Field(default="", description="若需澄清，反问什么")


class IntentClassifier:
    """
    意图识别器（多意图 + 情绪 + 紧迫度联合识别）

    🎯 设计要点：
    1. 使用结构化输出（强制 JSON Schema）
    2. 一次 LLM 调用同时识别意图+情绪+紧迫度（节省成本）
    3. 置信度低于阈值时主动反问澄清
    4. 缓存常见 query 的识别结果（Redis）
    """

    def __init__(self, llm_client, cache_client, confidence_threshold=0.7):
        self.llm = llm_client
        self.cache = cache_client
        self.threshold = confidence_threshold

    async def classify(self, user_input: str, history: list = None) -> IntentResult:
        # 1. 检查缓存
        cache_key = f"intent:{hash(user_input)}"
        cached = await self.cache.get(cache_key)
        if cached:
            return IntentResult.parse_raw(cached)

        # 2. 构造 Prompt（带 few-shot 示例）
        prompt = self._build_prompt(user_input, history)

        # 3. 调用 LLM 强制输出 JSON
        response = await self.llm.chat.completions.create(
            model=settings.llm_router_model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        result = IntentResult.parse_raw(response.choices[0].message.content)

        # 4. 缓存结果（24小时）
        await self.cache.setex(cache_key, 86400, result.json())

        return result