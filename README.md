# 🏛️ Athena - 个人成长教练 Agent 系统

> 基于 LangGraph 的生产级多 Agent 协作平台，集成意图识别、语义路由、MCP 工具协议、分层记忆系统、监控 Agent 与端到端评测体系。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 **在线 Dem
o**: [https://athena.yourdomain.com](https://athena.yourdomain.com)
📺 **演示视频**: [Bilibili 链接](https://www.bilibili.com/)
📝 **技术博客**: [设计文档](docs/ARCHITECTURE.md)

---

## ✨ 核心亮点

- 🎯 **七层架构设计**：意图识别 → 语义路由 → Worker Agent → MCP 工具层 → 分层记忆 → 监控 Agent → 评测体系
- 🚀 **生产级工程**：Docker 容器化、Nginx + HTTPS、健康检查、限流、监控告警全配齐
- 🧠 **分层记忆系统**：短期（Redis）+ 摘要（LLM Summary）+ 长期（Qdrant 向量库）+ 情景记忆四层管理
- 🔧 **MCP 协议接入**：基于 Anthropic 2025 业界标准 Model Context Protocol，统一工具调用层
- 👁️ **元 Agent 监控**：实时检测主 Agent 跑题、循环、用户情绪恶化，自动介入兜底
- 📊 **端到端评测**：LLM-as-a-Judge + Ragas 多维度评分，含 50+ 测试 Case 与 20+ Bad Case 调优记录

---

## 🏗️ 系统架构

\`\`\`
      用户输入
         │
         ▼
   ┌─────────────┐
   │ 意图识别层   │  ← LLM 结构化输出（intent + emotion + urgency）
   └──────┬──────┘
          ▼
   ┌─────────────┐
   │ 语义路由层   │  ← 双路决策：意图匹配 + Embedding 相似度
   └──────┬──────┘
          ▼
   ┌─────────────────────────────────────┐
   │ Worker Agent 集群                    │
   │ 学习教练 / 健身教练 / 心理教练 / 目标管理 │
   └──────┬──────────────────────────────┘
          ▼
   ┌─────────────┐    ┌──────────────┐
   │ MCP 工具层   │    │ 分层记忆系统  │
   │ Notion/Cal..│    │ Redis/Qdrant │
   └─────────────┘    └──────────────┘
          │
          ▼
   ┌─────────────┐
   │ 监控 Agent  │  ← 实时监控异常并介入
   └─────────────┘
\`\`\`

---

## 📊 关键指标（持续优化中）

| 指标 | 初始值 | 当前值 | 目标 |
|---|---|---|---|
| 意图识别准确率 | 72% | **91%** | 95% |
| 路由准确率 | 60% | **89%** | 95% |
| 工具调用成功率 | 78% | **96%** | 99% |
| 端到端任务完成率 | 55% | **84%** | 90% |
| 平均响应时间 (P95) | 4.2s | **1.8s** | <2s |

---

## 🚀 快速开始

### 本地开发

\`\`\`bash
# 1. 克隆项目
git clone https://github.com/yourname/athena-agent.git
cd athena-agent

# 2. 创建环境配置
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 3. 一键启动所有服务
docker-compose -f docker/docker-compose.yml up -d

# 4. 访问 API 文档
open http://localhost:8000/docs
\`\`\`

### 服务器部署

详见 [部署文档](docs/DEPLOYMENT.md)

---

## 📁 项目结构

\`\`\`
athena-agent/
├── athena/          # 核心业务代码
│   ├── agents/      # 各类 Worker Agent
│   ├── core/        # 意图识别、路由、编排器
│   ├── memory/      # 分层记忆系统
│   ├── tools/       # MCP 工具集
│   ├── evaluation/  # 评测体系
│   └── api/         # FastAPI 接口
├── docs/            # 设计文档与 Bad Case 记录
├── tests/           # 单元测试
└── docker/          # 容器化配置
\`\`\`

---

## 🛠️ 技术栈

- **Agent 框架**: LangGraph 0.2+
- **Web 框架**: FastAPI + Uvicorn + Gunicorn
- **LLM**: GLM-4-Flash / Qwen-Plus / DeepSeek-V3
- **Embedding**: bge-m3 (本地)
- **向量库**: Qdrant
- **关系库**: PostgreSQL 16
- **缓存**: Redis 7
- **工具协议**: MCP (Model Context Protocol)
- **监控**: LangSmith + Sentry + Prometheus + Grafana
- **评测**: Ragas + DeepEval + LLM-as-a-Judge

---

## 📈 开发路线图

- [x] 第 1-2 周：基础设施 + 单 Agent MVP
- [x] 第 3-4 周：意图识别 + 语义路由
- [ ] 第 5-6 周：多 Agent 集群 + MCP 工具
- [ ] 第 7-8 周：分层记忆系统
- [ ] 第 9-10 周：监控 Agent + 评测体系
- [ ] 第 11-12 周：Bad Case 调优 + 技术博客

详见 [开发计划](docs/ROADMAP.md)

---

## 📚 设计文档

- [架构设计](docs/ARCHITECTURE.md)
- [Bad Case 调优记录](docs/BAD_CASES.md)（**面试重点**）
- [评测报告](docs/EVALUATION_REPORT.md)
- [部署指南](docs/DEPLOYMENT.md)

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 联系作者

- 📧 Email: your.email@example.com
- 🔗 GitHub: [@yourname](https://github.com/yourname)
- 📝 个人博客: [yourblog.com](https://yourblog.com)