"""LangGraph 全局 State 定义"""

from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
import operator


class AthenaState(TypedDict):
    """
    Athena 多 Agent 系统的全局状态

    第一周只用基础字段，后续会扩展：
    - intent (意图识别结果)
    - selected_agent (路由结果)
    - memory_context (记忆上下文)
    """
    user_input: str  # 用户输入
    user_id: str  # 用户ID
    session_id: str  # 会话ID
    messages: Annotated[List[BaseMessage], operator.add]  # 对话历史
    reply: str  # 最终回复