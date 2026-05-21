class SemanticRouter:
    """
    语义路由器：基于 Embedding 相似度 + 意图分类双重决策

    🎯 设计亮点（面试可讲）：
    1. 双路决策：意图匹配 + 向量相似度
    2. 置信度阈值兜底（低于 0.6 走兜底 Agent）
    3. 多 Agent 投票机制（多个 Agent 都能处理时按 Topk 排序）
    4. 路由准确率持续监控（每个路由决策都记录到 LangSmith）
    """

    AGENT_DESCRIPTIONS = {
        "learning_coach": "回答学习问题、解释概念、出题、规划学习路径",
        "fitness_coach": "制定健身计划、纠正动作、追踪健康数据",
        "psychology_coach": "情绪支持、共情陪伴、引导认知重构",
        "goal_manager": "OKR管理、目标分解、进度追踪、复盘",
    }

    def __init__(self, embedding_client, qdrant_client):
        self.embedder = embedding_client
        self.qdrant = qdrant_client
        # 预计算所有 Agent 描述的 Embedding，存入 Qdrant
        self._init_agent_embeddings()

    async def route(self, user_input: str, intent: IntentResult) -> dict:
        # 双路决策
        # 路径1：基于意图直接映射
        intent_route = self._intent_based_route(intent)

        # 路径2：基于 Embedding 相似度
        semantic_route = await self._semantic_route(user_input)

        # 融合决策
        return self._merge_decisions(intent_route, semantic_route, intent.confidence)