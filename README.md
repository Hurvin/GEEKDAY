# 潮韵云脑 (Chaoyun Yunnao) 🌊🤖

<div align="center">
  <img src="./logo.png" alt="Logo" width="120" />
  <br />
  <p><b>基于大模型的潮汕文化智慧旅行助手</b></p>
  <p>
    <a href="#-核心功能">核心功能</a> •
    <a href="#-技术栈">技术栈</a> •
    <a href="#-快速开始">快速开始</a> •
    <a href="#-系统架构">系统架构</a>
  </p>
</div>

---

**潮韵云脑** 也就是 **潮韵同行 (Chaoyun Tongxing)**，是一个结合了**生成式 AI** 与**潮汕本土文化知识库**的智能文旅 Agent MVP 项目。

它不仅能为你生成个性化的潮汕旅游行程，还能像当地向导一样，根据实时的天气、人流量变化动态调整计划，并提供避坑指南和文化科普。

## ✨ 核心功能

- **🧠 智能行程规划**：基于 LangGraph 和 LLM（支持 Qwen, DeepSeek, Hunyuan 等），根据你的偏好（如“美食”、“文化体验”）生成详细行程。
- **🌦️ 动态应变引擎**：模拟真实旅行中的突发状况（如突降暴雨、景点拥挤），Agent 会实时感知并建议调整行程。
- **🛡️ 避坑与文化雷达**：内置潮汕文化规则库（如“下午茶文化”、“祭祀禁忌”）和避坑指南，让你的旅行地道又安心。
- **💾 三层记忆系统**：
  - **短期记忆**：流畅的对话上下文。
  - **中期记忆**：结构化的行程数据（JSON）。
  - **长期记忆**：用户画像与固化的文化规则。
- **🔌 MCP Server 集成**：提供标准化的 Model Context Protocol (MCP) 工具接口，支持 `plan_trip`, `get_culture_hint`, `risk_check` 等能力。

## 🛠 技术栈

### Frontend (前端)
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI/样式**: 自定义 CSS Variables, 响应式设计
- **交互**: 实时流式对话，动态地图/行程卡片

### Backend (后端)
- **框架**: FastAPI
- **Agent编排**: LangGraph + LangChain Core
- **LLM 接入**: OpenAI SDK (对接 Sophnet API，支持 Qwen2.5, DeepSeek-V3/R1 等)
- **协议**: MCP (Model Context Protocol)
- **数据验证**: Pydantic

## 🚀 快速开始

### 1. 环境准备

- Python >= 3.11
- Node.js >= 18
- 获取 [Sophnet](https://www.sophnet.com/) API Key (或其他兼容 OpenAI 格式的 API Key)

### 2. 后端启动

```bash
# 进入后端目录
cd backend

# 复制环境变量配置
cp .env.example .env
# 编辑 .env 文件，填入你的 SOPHNET_API_KEY

# 安装依赖
pip install -e ".[dev]"

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 3. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问浏览器 [http://localhost:5173](http://localhost:5173) 即可开始体验。

### 4. Docker 一键启动

```bash
# 在项目根目录
docker compose up --build
```

## 🎮 功能演示与调试

### 模拟突发事件 (Fake Events)

为了演示 Agent 的动态调整能力，我们提供了一个 CLI 工具来模拟环境变化：

**模拟天气变化：**
```bash
# 在 backend 目录下执行
python scripts/fake_event_cli.py --type weather --destination 潮州 --day 1 --old 晴朗 --new 雷阵雨 --note "模拟午后雷雨"
```
*效果：前端会收到通知，Agent 会建议将户外活动调整为室内（如茶馆）。*

**模拟人流拥堵：**
```bash
python scripts/fake_event_cli.py --type crowd --destination 汕头 --day 2 --old 中 --new 高
```

### API 接口

- **API 文档**: `http://localhost:8000/docs`
- **健康检查**: `GET /api/v1/health`

## 📂 项目结构

```text
.
├── backend/                # Python 后端 (FastAPI + LangGraph)
│   ├── app/
│   │   ├── agent/          # Agent 核心逻辑 (Tools, Graph, Nodes)
│   │   ├── services/       # 业务服务 (LLM, MCP, FakeEvents)
│   │   └── memory/         # 记忆存储 (JSON/Markdown)
│   └── scripts/            # 辅助脚本
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面视图 (Chat, Planner)
│   │   └── components/     # 组件
│   └── public/             # 静态资源
├── tp/                     # 演示图片资源
└── docker-compose.yml      # 容器编排
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

[MIT](LICENSE) © 2024 Chaoyun Yunnao Team
