import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from athena.core.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    user_id: str = Field(default="anonymous")
    session_id: str = Field(default="default")

class ChatResponse(BaseModel):
    reply: str
    user_id: str
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
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
        raise HTTPException(status_code=500, detail=str(e))
