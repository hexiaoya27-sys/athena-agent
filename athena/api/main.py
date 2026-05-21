import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from athena.api.routes.chat import router as chat_router
from athena.config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    logger.info(f"🚀 Athena 启动 [env={s.app_env}, model={s.llm_main_model}]")
    yield
    logger.info("👋 Athena 关闭")

app = FastAPI(
    title="Athena Agent System",
    description="个人成长教练多 Agent 协作系统",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"service": "Athena Agent System", "version": "0.1.0", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "athena-agent", "version": "0.1.0"}

app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
