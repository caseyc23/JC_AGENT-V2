
![new_header](https://github.com/user-attachments/assets/e236b764-0ddc-42ff-a1f1-8fbb3d2e0e65)


<div align="center">
<a href="https://discord.gg/ejRNvftDp9">
<img src="https://img.shields.io/discord/1359368468260192417" alt="Discord">
</a>
</div>

<div align="center">

[English](README.md) | [简体中文](README.zh-CN.md)

</div>

# SurfSense
Connect any LLM to your internal knowledge sources and chat with it in real time alongside your team. OSS alternative to NotebookLM, Perplexity, and Glean.

SurfSense is a highly customizable AI research agent, connected to external sources such as Search Engines (SearxNG, Tavily, LinkUp), Google Drive, Slack, Linear, Jira, ClickUp, Confluence, BookStack, Gmail, Notion, YouTube, GitHub, Discord, Airtable, Google Calendar, Luma, Circleback, Elasticsearch and more to come.

<div align="center">
<a href="https://trendshift.io/repositories/13606" target="_blank"><img src="https://trendshift.io/api/badge/repositories/13606" alt="MODSetter%2FSurfSense | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>


# Video 

https://github.com/user-attachments/assets/42a29ea1-d4d8-4213-9c69-972b5b806d58



## Podcast Sample

https://github.com/user-attachments/assets/a0a16566-6967-4374-ac51-9b3e07fbecd7




## Key Features

### 💡 **Idea**: 
- Open source alternative to NotebookLM, Perplexity, and Glean. Connect any LLM to your internal knowledge sources and collaborate with your team in real time.
### 📁 **Multiple File Format Uploading Support**
- Save content from your own personal files *(Documents, images, videos and supports **50+ file extensions**)* to your own personal knowledge base .
### 🔍 **Powerful Search**
- Quickly research or find anything in your saved content .
### 💬 **Chat with your Saved Content**
- Interact in Natural Language and get cited answers.
### 📄 **Cited Answers**
- Get Cited answers just like Perplexity.
### 🔔 **Privacy & Local LLM Support**
- Works Flawlessly with Ollama local LLMs.
### 🏠 **Self Hostable**
- Open source and easy to deploy locally.
### 👥 **Team Collaboration with RBAC**
- Role-Based Access Control for Search Spaces
- Invite team members with customizable roles (Owner, Admin, Editor, Viewer)
- Granular permissions for documents, chats, connectors, and settings
- Share knowledge bases securely within your organization
### 🎙️ Podcasts 
- Blazingly fast podcast generation agent. (Creates a 3-minute podcast in under 20 seconds.)
- Convert your chat conversations into engaging audio content
- Support for local TTS providers (Kokoro TTS)
- Support for multiple TTS providers (OpenAI, Azure, Google Vertex AI)

### 🤖 **Deep Agent Architecture**

#### Built-in Agent Tools
| Tool | Description |
|------|-------------|
| **search_knowledge_base** | Search your personal knowledge base with semantic + full-text hybrid search, date filtering, and connector-specific queries |
| **generate_podcast** | Generate audio podcasts from chat conversations or knowledge base content |
| **link_preview** | Fetch rich Open Graph metadata for URLs to display preview cards |
| **display_image** | Display images in chat with metadata and source attribution |
| **scrape_webpage** | Extract full content from webpages for analysis and summarization (supports Firecrawl or local Chromium/Trafilatura) |

#### Extensible Tools Registry
Contributors can easily add new tools via the registry pattern:
1. Create a tool factory function in `surfsense_backend/app/agents/new_chat/tools/`
2. Register it in the `BUILTIN_TOOLS` list in `registry.py`

#### Configurable System Prompts
- Custom system instructions via LLM configuration
- Toggle citations on/off per configuration
- Supports 100+ LLMs via LiteLLM integration

### 📊 **Advanced RAG Techniques**
- Supports 100+ LLM's
- Supports 6000+ Embedding Models.
- Supports all major Rerankers (Pinecone, Cohere, Flashrank etc)
- Uses Hierarchical Indices (2 tiered RAG setup).
- Utilizes Hybrid Search (Semantic + Full Text Search combined with Reciprocal Rank Fusion).

### ℹ️ **External Sources**
- Search Engines (Tavily, LinkUp)
- SearxNG (self-hosted instances)
- Google Drive
- Slack
- Linear
- Jira
- ClickUp
- Confluence
- BookStack
- Notion
- Gmail
- Youtube Videos
- GitHub
- Discord
- Airtable
- Google Calendar
- Luma
- Circleback
- Elasticsearch
- and more to come.....

## 📄 **Supported File Extensions**

| ETL Service | Formats | Notes |
|-------------|---------|-------|
| **LlamaCloud** | 50+ formats | Documents, presentations, spreadsheets, images |
| **Unstructured** | 34+ formats | Core formats + email support |
| **Docling** | Core formats | Local processing, no API key required |

**Audio/Video** (via STT Service): `.mp3`, `.wav`, `.mp4`, `.webm`, etc.

### 🔖 Cross Browser Extension
- The SurfSense extension can be used to save any webpage you like.
- Its main usecase is to save any webpages protected beyond authentication.



## FEATURE REQUESTS AND FUTURE


**SurfSense is actively being developed.** While it's not yet production-ready, you can help us speed up the process.

Join the [SurfSense Discord](https://discord.gg/ejRNvftDp9) and help shape the future of SurfSense!

## 🚀 Roadmap

Stay up to date with our development progress and upcoming features!  
Check out our public roadmap and contribute your ideas or feedback:

**📋 Roadmap Discussion:** [SurfSense 2025-2026 Roadmap: Deep Agents, Real-Time Collaboration & MCP Servers](https://github.com/MODSetter/SurfSense/discussions/565)

**📊 Kanban Board:** [SurfSense Project Board](https://github.com/users/MODSetter/projects/3)


## How to get started?

### Quick Start with Docker 🐳

> [!TIP]
> For production deployments, use the full [Docker Compose setup](https://www.surfsense.com/docs/docker-installation) which offers more control and scalability.

**Linux/macOS:**

```bash
docker run -d -p 3000:3000 -p 8000:8000 \
  -v surfsense-data:/data \
  --name surfsense \
  --restart unless-stopped \
  ghcr.io/modsetter/surfsense:latest
```

**Windows (PowerShell):**

```powershell
docker run -d -p 3000:3000 -p 8000:8000 `
  -v surfsense-data:/data `
  --name surfsense `
  --restart unless-stopped `
  ghcr.io/modsetter/surfsense:latest
```

**With Custom Configuration:**

You can pass any environment variable using `-e` flags:

```bash
docker run -d -p 3000:3000 -p 8000:8000 \
  -v surfsense-data:/data \
  -e EMBEDDING_MODEL=openai://text-embedding-ada-002 \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e AUTH_TYPE=GOOGLE \
  -e GOOGLE_OAUTH_CLIENT_ID=your_google_client_id \
  -e GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret \
  -e ETL_SERVICE=LLAMACLOUD \
  -e LLAMA_CLOUD_API_KEY=your_llama_cloud_key \
  --name surfsense \
  --restart unless-stopped \
  ghcr.io/modsetter/surfsense:latest
```

> [!NOTE]
> - If deploying behind a reverse proxy with HTTPS, add `-e BACKEND_URL=https://api.yourdomain.com`

After starting, access SurfSense at:
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

**Useful Commands:**

```bash
docker logs -f surfsense      # View logs
docker stop surfsense         # Stop
docker start surfsense        # Start
docker rm surfsense           # Remove (data preserved in volume)
```

### Installation Options

SurfSense provides multiple options to get started:

1. **[SurfSense Cloud](https://www.surfsense.com/login)** - The easiest way to try SurfSense without any setup.
   - No installation required
   - Instant access to all features
   - Perfect for getting started quickly

2. **Quick Start Docker (Above)** - Single command to get SurfSense running locally.
   - All-in-one image with PostgreSQL, Redis, and all services bundled
   - Perfect for evaluation, development, and small deployments
   - Data persisted via Docker volume

3. **[Docker Compose (Production)](https://www.surfsense.com/docs/docker-installation)** - Full stack deployment with separate services.
   - Includes pgAdmin for database management through a web UI
   - Supports environment variable customization via `.env` file
   - Flexible deployment options (full stack or core services only)
   - Better for production with separate scaling of services

4. **[Manual Installation](https://www.surfsense.com/docs/manual-installation)** - For users who prefer more control over their setup or need to customize their deployment.

Docker and manual installation guides include detailed OS-specific instructions for Windows, macOS, and Linux.

Before self-hosting installation, make sure to complete the [prerequisite setup steps](https://www.surfsense.com/docs/) including:
- Auth setup (optional - defaults to LOCAL auth)
- **File Processing ETL Service** (optional - defaults to Docling):
  - Docling (default, local processing, no API key required, supports PDF, Office docs, images, HTML, CSV)
  - Unstructured.io API key (supports 34+ formats)
  - LlamaIndex API key (enhanced parsing, supports 50+ formats)
- Other API keys as needed for your use case



## Tech Stack


 ### **BackEnd** 

-  **FastAPI**: Modern, fast web framework for building APIs with Python
  
-  **PostgreSQL with pgvector**: Database with vector search capabilities for similarity searches

-  **SQLAlchemy**: SQL toolkit and ORM (Object-Relational Mapping) for database interactions

-  **Alembic**: A database migrations tool for SQLAlchemy.

-  **FastAPI Users**: Authentication and user management with JWT and OAuth support

-  **Deep Agents**: Custom agent framework built on LangGraph for reasoning and acting AI agents with configurable tools

-  **LangGraph**: Framework for developing stateful AI agents with conversation persistence

-  **LangChain**: Framework for developing AI-powered applications.

-  **LiteLLM**: Universal LLM integration supporting 100+ models (OpenAI, Anthropic, Ollama, etc.)

-  **Rerankers**: Advanced result ranking for improved search relevance

-  **Hybrid Search**: Combines vector similarity and full-text search for optimal results using Reciprocal Rank Fusion (RRF)

-  **Vector Embeddings**: Document and text embeddings for semantic search

-  **pgvector**: PostgreSQL extension for efficient vector similarity operations

-  **Redis**: In-memory data structure store used as message broker and result backend for Celery

-  **Celery**: Distributed task queue for handling asynchronous background jobs (document processing, podcast generation, etc.)

-  **Flower**: Real-time monitoring and administration tool for Celery task queues

-  **Chonkie**: Advanced document chunking and embedding library

  
---
 ### **FrontEnd**

-  **Next.js**: React framework featuring App Router, server components, automatic code-splitting, and optimized rendering.

-  **React**: JavaScript library for building user interfaces.

-  **TypeScript**: Static type-checking for JavaScript, enhancing code quality and developer experience.

- **Vercel AI SDK Kit UI Stream Protocol**: To create scalable chat UI.

-  **Tailwind CSS**: Utility-first CSS framework for building custom UI designs.

-  **Shadcn**: Headless components library.

-  **Motion (Framer Motion)**: Animation library for React.



 ### **DevOps**

-  **Docker**: Container platform for consistent deployment across environments
  
-  **Docker Compose**: Tool for defining and running multi-container Docker applications

-  **pgAdmin**: Web-based PostgreSQL administration tool included in Docker setup


### **Extension** 
 Manifest v3 on Plasmo


## Contribute 

Contributions are very welcome! A contribution can be as small as a ⭐ or even finding and creating issues.
Fine-tuning the Backend is always desired.

### Adding New Agent Tools

Want to add a new tool to the SurfSense agent? It's easy:

1. Create your tool file in `surfsense_backend/app/agents/new_chat/tools/my_tool.py`
2. Register it in `registry.py`:

```python
ToolDefinition(
    name="my_tool",
    description="What my tool does",
    factory=lambda deps: create_my_tool(
        search_space_id=deps["search_space_id"],
        db_session=deps["db_session"],
    ),
    requires=["search_space_id", "db_session"],
),
```

For detailed contribution guidelines, please see our [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Star History

<a href="https://www.star-history.com/#MODSetter/SurfSense&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=MODSetter/SurfSense&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=MODSetter/SurfSense&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=MODSetter/SurfSense&type=Date" />
 </picture>
</a>

---
---
<p align="center">
    <img 
      src="https://github.com/user-attachments/assets/329c9bc2-6005-4aed-a629-700b5ae296b4" 
      alt="Catalyst Project" 
      width="200"
    />
</p>

---
---


---

# docs/chinese-llm-setup.md

# 国产 LLM 配置指南 | Chinese LLM Setup Guide

本指南将帮助你在 SurfSense 中配置和使用国产大语言模型。

This guide helps you configure and use Chinese LLM providers in SurfSense.

---

## 📋 支持的提供商 | Supported Providers

SurfSense 现已支持以下国产 LLM：

- ✅ **DeepSeek** - 国产高性能 AI 模型
- ✅ **阿里通义千问 (Alibaba Qwen)** - 阿里云通义千问大模型
- ✅ **月之暗面 Kimi (Moonshot)** - 月之暗面 Kimi 大模型
- ✅ **智谱 AI GLM (Zhipu)** - 智谱 AI GLM 系列模型

---

## 🚀 快速开始 | Quick Start

### 通用配置步骤 | General Configuration Steps

1. 登录 SurfSense Dashboard
2. 进入 **Settings** → **API Keys** (或 **LLM Configurations**)
3. 点击 **Add New Configuration**
4. 从 **Provider** 下拉菜单中选择你的国产 LLM 提供商
5. 填写必填字段（见下方各提供商详细配置）
6. 点击 **Save**

---

## 1️⃣ DeepSeek 配置 | DeepSeek Configuration

### 获取 API Key

1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 进入 **API Keys** 页面
4. 点击 **Create New API Key**
5. 复制生成的 API Key (格式: `sk-xxx`)

### 在 SurfSense 中配置

| 字段 | 值 | 说明 |
|------|-----|------|
| **Configuration Name** | `DeepSeek Chat` | 配置名称（自定义） |
| **Provider** | `DEEPSEEK` | 选择 DeepSeek |
| **Model Name** | `deepseek-chat` | 推荐模型<br>其他选项: `deepseek-coder` |
| **API Key** | `sk-xxx...` | 你的 DeepSeek API Key |
| **API Base URL** | `https://api.deepseek.com` | DeepSeek API 地址 |
| **Parameters** | _(留空)_ | 使用默认参数 |

### 示例配置

```
Configuration Name: DeepSeek Chat
Provider: DEEPSEEK
Model Name: deepseek-chat
API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API Base URL: https://api.deepseek.com
```

### 可用模型

- **deepseek-chat**: 通用对话模型（推荐）
- **deepseek-coder**: 代码专用模型

### 定价
- 请访问 [DeepSeek 定价页面](https://platform.deepseek.com/pricing) 查看最新价格

---

## 2️⃣ 阿里通义千问 (Alibaba Qwen) 配置

### 获取 API Key

1. 访问 [阿里云百炼平台](https://dashscope.aliyun.com/)
2. 登录阿里云账号
3. 开通 DashScope 服务
4. 进入 **API-KEY 管理**
5. 创建并复制 API Key

### 在 SurfSense 中配置

| 字段 | 值 | 说明 |
|------|-----|------|
| **Configuration Name** | `通义千问 Max` | 配置名称（自定义） |
| **Provider** | `ALIBABA_QWEN` | 选择阿里通义千问 |
| **Model Name** | `qwen-max` | 推荐模型<br>其他选项: `qwen-plus`, `qwen-turbo` |
| **API Key** | `sk-xxx...` | 你的 DashScope API Key |
| **API Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 阿里云 API 地址 |
| **Parameters** | _(留空)_ | 使用默认参数 |

### 示例配置

```
Configuration Name: 通义千问 Max
Provider: ALIBABA_QWEN
Model Name: qwen-max
API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 可用模型

- **qwen-max**: 最强性能，适合复杂任务
- **qwen-plus**: 性价比高，适合日常使用（推荐）
- **qwen-turbo**: 速度快，适合简单任务

### 定价
- 请访问 [阿里云百炼定价](https://help.aliyun.com/zh/model-studio/getting-started/billing) 查看最新价格

---

## 3️⃣ 月之暗面 Kimi (Moonshot) 配置

### 获取 API Key

1. 访问 [Moonshot AI 开放平台](https://platform.moonshot.cn/)
2. 注册并登录账号
3. 进入 **API Key 管理**
4. 创建新的 API Key
5. 复制 API Key

### 在 SurfSense 中配置

| 字段 | 值 | 说明 |
|------|-----|------|
| **Configuration Name** | `Kimi` | 配置名称（自定义） |
| **Provider** | `MOONSHOT` | 选择月之暗面 Kimi |
| **Model Name** | `moonshot-v1-32k` | 推荐模型<br>其他选项: `moonshot-v1-8k`, `moonshot-v1-128k` |
| **API Key** | `sk-xxx...` | 你的 Moonshot API Key |
| **API Base URL** | `https://api.moonshot.cn/v1` | Moonshot API 地址 |
| **Parameters** | _(留空)_ | 使用默认参数 |

### 示例配置

```
Configuration Name: Kimi 32K
Provider: MOONSHOT
Model Name: moonshot-v1-32k
API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API Base URL: https://api.moonshot.cn/v1
```

### 可用模型

- **moonshot-v1-8k**: 8K 上下文（基础版）
- **moonshot-v1-32k**: 32K 上下文（推荐）
- **moonshot-v1-128k**: 128K 上下文（长文本专用）

### 定价
- 请访问 [Moonshot AI 定价](https://platform.moonshot.cn/pricing) 查看最新价格

---

## 4️⃣ 智谱 AI GLM (Zhipu) 配置

### 获取 API Key

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 进入 **API 管理**
4. 创建新的 API Key
5. 复制 API Key

### 在 SurfSense 中配置

| 字段 | 值 | 说明 |
|------|-----|------|
| **Configuration Name** | `GLM-4` | 配置名称（自定义） |
| **Provider** | `ZHIPU` | 选择智谱 AI |
| **Model Name** | `glm-4` | 推荐模型<br>其他选项: `glm-4-flash`, `glm-3-turbo` |
| **API Key** | `xxx.yyy...` | 你的智谱 API Key |
| **API Base URL** | `https://open.bigmodel.cn/api/paas/v4` | 智谱 API 地址 |
| **Parameters** | _(留空)_ | 使用默认参数 |

### 示例配置

```
Configuration Name: GLM-4
Provider: ZHIPU
Model Name: glm-4
API Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
API Base URL: https://open.bigmodel.cn/api/paas/v4
```

### 可用模型

- **glm-4**: GLM-4 旗舰模型（推荐）
- **glm-4-flash**: 快速推理版本
- **glm-3-turbo**: 高性价比版本

### 定价
- 请访问 [智谱 AI 定价](https://open.bigmodel.cn/pricing) 查看最新价格

---

## ⚙️ 高级配置 | Advanced Configuration

### 自定义参数 | Custom Parameters

你可以在 **Parameters** 字段中添加自定义参数（JSON 格式）：

```json
{
  "temperature": 0.7,
  "max_tokens": 2000,
  "top_p": 0.9
}
```

### 常用参数说明

| 参数 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| `temperature` | 控制输出随机性，越高越随机 | 0.7 | 0.0 - 1.0 |
| `max_tokens` | 最大输出 Token 数 | 模型默认 | 1 - 模型上限 |
| `top_p` | 核采样参数 | 1.0 | 0.0 - 1.0 |

---

## 🔧 故障排除 | Troubleshooting

### 常见问题

#### 1. **错误: "Invalid API Key"**
- ✅ 检查 API Key 是否正确复制（无多余空格）
- ✅ 确认 API Key 是否已激活
- ✅ 检查账户余额是否充足

#### 2. **错误: "Connection timeout"**
- ✅ 确认 API Base URL 是否正确
- ✅ 检查网络连接
- ✅ 确认防火墙是否允许访问

#### 3. **错误: "Model not found"**
- ✅ 确认模型名称是否拼写正确
- ✅ 检查该模型是否已开通
- ✅ 参照上方文档确认可用模型名称

#### 4. **文档处理卡住 (IN_PROGRESS)**
- ✅ 检查模型名称中是否有多余空格
- ✅ 确认 API Key 有效且有额度
- ✅ 查看后端日志: `docker compose logs backend`

### 查看日志

```bash
# 查看后端日志
docker compose logs backend --tail 100

# 实时查看日志
docker compose logs -f backend

# 搜索错误
docker compose logs backend | grep -i "error"
```

---

## 💡 最佳实践 | Best Practices

### 1. 模型选择建议

| 任务类型 | 推荐模型 | 说明 |
|---------|---------|------|
| **文档摘要** | Qwen-Plus, GLM-4 | 平衡性能和成本 |
| **代码分析** | DeepSeek-Coder | 代码专用 |
| **长文本处理** | Kimi 128K | 超长上下文 |
| **快速响应** | Qwen-Turbo, GLM-4-Flash | 速度优先 |

### 2. 成本优化

- 🎯 **Long Context LLM**: 使用 Qwen-Plus 或 GLM-4（处理文档摘要）
- ⚡ **Fast LLM**: 使用 Qwen-Turbo 或 GLM-4-Flash（快速对话）
- 🧠 **Strategic LLM**: 使用 Qwen-Max 或 DeepSeek-Chat（复杂推理）

### 3. API Key 安全

- ❌ 不要在公开代码中硬编码 API Key
- ✅ 定期轮换 API Key
- ✅ 为不同用途创建不同的 Key
- ✅ 设置合理的额度限制

---

## 📚 相关资源 | Resources

### 官方文档

- [DeepSeek 文档](https://platform.deepseek.com/docs)
- [阿里云百炼文档](https://help.aliyun.com/zh/model-studio/)
- [Moonshot AI 文档](https://platform.moonshot.cn/docs)
- [智谱 AI 文档](https://open.bigmodel.cn/dev/api)

### SurfSense 文档

- [安装指南](../README.md)
- [贡献指南](../CONTRIBUTING.md)
- [部署指南](../DEPLOYMENT_GUIDE.md)

---

## 🆘 需要帮助？ | Need Help?

如果遇到问题，可以通过以下方式获取帮助：

- 💬 [GitHub Issues](https://github.com/MODSetter/SurfSense/issues)
- 💬 [Discord Community](https://discord.gg/ejRNvftDp9)
- 📧 Email: [项目维护者邮箱]

---

## 🔄 更新日志 | Changelog

- **2025-01-12**: 初始版本，添加 DeepSeek、Qwen、Kimi、GLM 支持

---

**祝你使用愉快！Happy coding with Chinese LLMs! 🚀**

