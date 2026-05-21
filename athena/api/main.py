"""FastAPI 应用入口"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from athena.api.routes.chat import router as chat_router
from athena.config.settings import get_settings

# ===== 日志配置 =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


# ===== 生命周期管理 =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"🚀 Athena 启动中 [env={settings.app_env}]")
    logger.info(f"   LLM 主模型: {settings.llm_main_model}")
    yield
    logger.info("👋 Athena 关闭中...")


# ===== 创建 FastAPI 应用 =====
app = FastAPI(
    title="Athena Agent System",
    description="个人成长教练多 Agent 协作系统",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# ===== CORS 中间件 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== 核心端点 =====

@app.get("/", summary="服务信息")
async def root():
    return {
        "service": "Athena Agent System",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", summary="健康检查 - 第一周关键交付物 ✅")
async def health_check():
    """
    健康检查端点

    用途：
    - Docker HEALTHCHECK
    - 负载均衡器探活
    - 监控系统检测
    """
    return {
        "status": "healthy",
        "service": "athena-agent",
        "version": "0.1.0"
    }


# ===== 注册业务路由 =====
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])