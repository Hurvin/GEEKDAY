# 潮韵云脑 MVP

基于《项目计划书1229》的黑客松 MVP，包含：

- 前端：Vue 3 + Vite
- 后端：FastAPI + LangGraph
- Agent：潮汕文化规则 + 动态行程引擎 + 避坑雷达
- 协议：提供 REST API 与 MCP Server 工具能力

## 1. 目录结构

```text
.
├─ frontend/                 # Vue 前端
├─ backend/                  # Python 后端
├─ .env.example              # 环境变量模板
└─ docker-compose.yml        # 一键容器启动
```

## 2. 环境准备

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 填入你的 `SOPHNET_API_KEY`（不填则自动走本地兜底输出）。

## 3. 本地启动（推荐）

### 启动后端

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。

## 4. Docker 启动

```bash
docker compose up --build
```

## 5. API 快速验证

### 健康检查

```bash
curl http://localhost:8000/api/v1/health
```

### 生成行程

```bash
curl -X POST http://localhost:8000/api/v1/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination":"汕头",
    "days":2,
    "travel_style":"轻松",
    "travelers":"朋友",
    "preferences":["美食","文化体验"],
    "constraints":["不赶路"],
    "budget_level":"中等"
  }'
```

## 6. MCP Server

已在 `backend/app/services/mcp_server.py` 提供工具：

- `plan_trip`
- `get_culture_hint`
- `risk_check`

启动方式：

```bash
cd backend
python -m app.services.mcp_server
```

## 7. Active Context Compression

聊天接口 `/api/v1/chat` 已启用三层记忆：

- 短期记忆：最近 3 轮原始对话（保留细节）
- 中期记忆：已确认行程片段，压缩为结构化 JSON
- 长期记忆：用户偏好与文化规则固化到文档

相关文档文件：

- `backend/app/memory/long_term_memory.json`
- `backend/app/memory/long_term_memory.md`
- `backend/app/memory/mid_term_memory.json`
