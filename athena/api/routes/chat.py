"""聊天 API 路由"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from athena.core.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., min_length=1, max_length=2000, description="用户输入")
    user_id: str = Field(default="anonymous", description="用户ID")
    session_id: str = Field(default="default", description="会话ID")


class ChatResponse(BaseModel):
    """聊天响应"""
    reply: str
    user_id: str
    session_id: str


@router.post("/chat", response_model=ChatResponse, summary="发送消息给 Athena")
async def chat(request: ChatRequest):
    """
    发送一条消息，获取 Athena 的回复。

    示例：
    ```
    POST /api/v1/chat
    {
        "message": "你好",
        "user_id": "user_001"
    }
    ```
    """
    try:
        orchestrator = get_orchestrator()
        result = await orchestrator.run(
            user_input=request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )
        return ChatResponse(
            reply=result["reply"],
            user_id=request.user_id,
            session_id=request.session_id
        )
    except Exception as e:
        logger.exception("Chat 处理失败")
        raise HTTPException(status_code=500, detail=f"内部错误: {str(e)}")