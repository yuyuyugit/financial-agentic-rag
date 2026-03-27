好的！我来帮你把整个项目拆解成**渐进式的小任务**，每个任务都可以独立实现和测试，方便你逐步完成并提交代码。

## 🎯 项目整体流程概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Financial Agentic RAG (分层 LLM 架构)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  用户输入                                                                    │
│      ↓                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Phase 1: Router (Claude Haiku)                                     │  │
│  │  - 模型: Haiku (最快/最便宜)                                         │  │
│  │  - 任务: 意图分类，只需输出 "simple" 或 "complex"                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│           │                                                                │
│     ┌─────┴─────┐                                                          │
│     ↓           ↓                                                          │
│  简单查询    复杂查询                                                        │
│     ↓           ↓                                                          │
│  ┌────────┐ ┌─────────────────────────────────────────────────────────┐   │
│  │Keyword │ │      Phase 2: Agent (分层内部策略)                       │   │
│  │Search  │ │                                                         │   │
│  └────────┘ │  ┌─────────────────────────────────────────────────┐   │   │
│            │  │ 2.1 Analyze Node (Claude Haiku)                  │   │   │
│            │  │ - 意图分析、子任务拆解                             │   │   │
│            │  │ - 输出结构化 JSON                                  │   │   │
│            │  └─────────────────────────────────────────────────┘   │   │
│            │                         ↓                              │   │
│            │  ┌─────────────────────────────────────────────────┐   │   │
│            │  │ 2.2 Retrieve Node (无 LLM 调用)                 │   │   │
│            │  │ - 调用 Phase 3 检索                              │   │   │
│            │  │ - 纯计算，无成本                                  │   │   │
│            │  └─────────────────────────────────────────────────┘   │   │
│            │                         ↓                              │   │
│            │  ┌─────────────────────────────────────────────────┐   │   │
│            │  │ 2.3 Tool Call Node (Claude Haiku)               │   │   │
│            │  │ - 判断是否需要工具调用                            │   │   │
│            │  │ - 选择并格式化工具参数                            │   │   │
│            │  └─────────────────────────────────────────────────┘   │   │
│            │                         ↓                              │   │
│            │  ┌─────────────────────────────────────────────────┐   │   │
│            │  │ 2.4 Generate Node (Claude Sonnet - 可选)        │   │   │
│            │  │ - 复杂推理场景用 Sonnet                           │   │   │
│            │  │ - 简单场景用 Haiku                                │   │   │
│            │  │ - 支持 Citations API 提供来源                     │   │   │
│            │  └─────────────────────────────────────────────────┘   │   │
│            └─────────────────────────────────────────────────────────┘   │
│                                      ↓                                    │
│            ┌─────────────────────────────────────────────────────────┐   │
│            │      Phase 3: Hybrid Search (Weaviate)                 │   │
│            │  - 向量检索 (text2vec-openai)                          │   │
│            │  - 关键词检索 (BM25)                                    │   │
│            │  - 图谱检索 (可选，用 Haiku 做实体抽取)                  │   │
│            └─────────────────────────────────────────────────────────┘   │
│                                      ↓                                    │
│                  返回答案 + 来源引用                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📋 拆解为 7 个 Phase，共 20+ 个小任务

---

## Phase 0: 项目初始化（基础设施）

### Task 0.1: 创建项目目录结构
```
financial-agentic-rag/
├── src/
│   ├── __init__.py
│   ├── router/
│   │   └── __init__.py
│   ├── agent/
│   │   └── __init__.py
│   ├── retrieval/
│   │   └── __init__.py
│   ├── tools/
│   │   └── __init__.py
│   ├── data/
│   │   └── __init__.py
│   └── api/
│       └── __init__.py
├── frontend/
├── scripts/
├── docs/
├── data_samples/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```


### 第七步：常用命令速查

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f [service-name]  # service-name: backend/frontend/weaviate

# 停止所有服务
docker-compose down

# 停止并删除数据卷（重置数据库）
docker-compose down -v

# 重新构建镜像
docker-compose build --no-cache

# 进入容器终端
docker exec -it financial-backend /bin/bash

# 查看运行中的容器
docker ps
```

---

## ✅ 完成检查清单

- [ ] Docker Desktop 已安装并运行
- [ ] VS Code 已安装并配置好插件
- [ ] 项目目录已创建
- [ ] 所有配置文件已创建
- [ ] `.env` 中已填入真实的 OpenAI API Key
- [ ] `docker-compose up -d` 成功启动
- [ ] 能访问 http://localhost:8501 看到前端界面
- [ ] 能访问 http://localhost:8000/docs 看到 API 文档
- [ ] 能访问 http://localhost:8080 看到 Weaviate 控制台

**恭喜！你的容器化开发环境已经搭建完成！** 接下来就可以开始实现 Router、Agent、检索等核心功能了。


项目阶段总览
Phase	内容	优先级
Phase 0	基础设施（Docker、依赖、API入口）	P0
Phase 1	LLM Router（意图路由 + 关键词检索）	P0
Phase 2	Agent 框架（LangGraph 状态机）	P0
Phase 3	混合检索（Weaviate 向量 + BM25）	P1
Phase 4	工具调用（股价、新闻、持仓）	P1
Phase 5	工业化文档	P2
Phase 6	完善打磨（README、示例数据）	P2
各阶段独立 Prompts
Phase 0 — 基础设施
P0-A: Docker + 依赖配置


Create the following files for a Python FastAPI + Weaviate + Streamlit project:

1. `requirements.txt` with: langgraph>=0.0.40, langchain>=0.1.0, langchain-anthropic>=0.1.0, weaviate-client>=3.24, fastapi>=0.104, uvicorn>=0.24, pydantic>=2.0, yfinance>=0.2.28, python-dotenv>=1.0, streamlit>=1.28, httpx>=0.25, tiktoken>=0.5

2. `Dockerfile` (python:3.11-slim, WORKDIR /app, install requirements, expose 8000, CMD uvicorn src.api.main:app)

3. `Dockerfile.frontend` (python:3.11-slim, install streamlit requests, expose 8501)

4. `docker-compose.yml` with 3 services:
   - weaviate: image semitechnologies/weaviate:1.24.1, ports 8080:8080, env AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true, DEFAULT_VECTORIZER_MODULE=text2vec-openai, ENABLE_MODULES=text2vec-openai
   - backend: build ., ports 8000:8000, env OPENAI_API_KEY and WEAVIATE_URL=http://weaviate:8080, depends_on weaviate
   - frontend: build Dockerfile.frontend, ports 8501:8501, env BACKEND_URL=http://backend:8000, depends_on backend

5. `.env.example`: ANTHROPIC_API_KEY=your-anthropic-api-key, WEAVIATE_URL=http://weaviate:8080, LOG_LEVEL=INFO

6. `.gitignore`: .env, __pycache__, .DS_Store, *.pyc, weaviate_data/, .vscode/, .idea/
P0-B: FastAPI 入口


Create `src/api/main.py` for a FastAPI application:
- App title: "Financial Agentic RAG API"
- GET / → {"message": "Financial Agentic RAG Demo", "status": "running"}
- GET /health → {"status": "healthy"}
- GET /test-weaviate → try connect to weaviate at env WEAVIATE_URL (default http://weaviate:8080) using weaviate-client v3, return {"status": "connected"} or {"status": "error", "error": str(e)}
- POST /chat → accepts {"query": str}, returns {"answer": "not implemented", "query_type": "unknown"} as placeholder

Also create `src/__init__.py` and `src/api/__init__.py` as empty files.
Phase 1 — Router
P1-A: QueryType + IntentRouter


Create `src/router/intent_router.py` for a financial RAG system.

Requirements:
- Define `QueryType` enum with values: SIMPLE, COMPLEX
- Define simple query keywords: ["我的资产", "持仓", "余额", "账户", "股价", "涨跌幅"]
- Class `IntentRouter` with method `route(query: str) -> QueryType`:
  - First check if any keyword appears in query → return SIMPLE
  - Otherwise call OpenAI (model gpt-4o-mini) with a prompt asking to classify the query as SIMPLE or COMPLEX for a financial assistant
  - SIMPLE = factual lookups (price, balance, holdings)
  - COMPLEX = analysis, comparison, prediction, multi-step reasoning
  - Parse LLM response and return QueryType
- Constructor takes `api_key: str = None` (falls back to OPENAI_API_KEY env var)

Also create `src/router/__init__.py` exporting `IntentRouter` and `QueryType`.
P1-B: 关键词检索


Create `src/retrieval/keyword_search.py` for a financial RAG system.

Requirements:
- Class `KeywordSearcher` with method `search(query: str) -> dict`:
  - Use a hardcoded mock dataset (dict) with keys like "资产", "持仓", "余额", "股价"
  - Match query against keys using simple substring search
  - Return {"result": str, "source": "keyword_search"} or {"result": "未找到相关信息", "source": "keyword_search"}
- Mock data should include realistic financial placeholders:
  - 总资产: "您的总资产为 ¥1,234,567.89"
  - 持仓: "当前持仓：茅台(600519) 100股，腾讯(0700.HK) 200股"
  - 余额: "可用余额：¥50,000.00"

Also create `src/retrieval/__init__.py`.
Phase 2 — Agent (LangGraph)
P2-A: Agent State


Create `src/agent/state.py` for a LangGraph-based financial agent.

Requirements:
- Import TypedDict, Annotated from typing; operator
- Define `AgentState(TypedDict)` with fields:
  - messages: Annotated[list, operator.add]  # chat history
  - query: str                                # original user query
  - intent: str                               # "analyze" | "retrieve" | "generate" | "done"
  - retrieved_docs: list[dict]               # documents from retrieval
  - tool_calls: list[dict]                   # tool invocations
  - final_answer: str                        # generated answer
  - iteration_count: int                     # prevent infinite loops

Also create `src/agent/__init__.py`.
P2-B: Agent Nodes


Create `src/agent/nodes.py` for a LangGraph financial agent.

Use langchain_openai.ChatOpenAI (model gpt-4o-mini, from OPENAI_API_KEY env).

Implement these functions, each takes `state: AgentState` and returns `dict` (partial state update):

1. `analyze_node(state)`: Call LLM with system prompt "You are a financial analyst. Analyze the query and decide next action: retrieve_docs or generate_answer." Set state["intent"] based on response.

2. `retrieve_node(state)`: Placeholder — return {"retrieved_docs": [{"content": f"Mock document for: {state['query']}", "source": "mock"}], "intent": "generate"}

3. `generate_node(state)`: Call LLM with the query + retrieved_docs context, return {"final_answer": llm_response, "intent": "done"}

4. `should_continue(state) -> str`: Return "retrieve" if intent=="retrieve", "generate" if intent=="generate", END if intent=="done" or iteration_count>3

Import AgentState from .state. Import END from langgraph.graph.
P2-C: LangGraph Graph


Create `src/agent/graph.py` to build a LangGraph StateGraph for a financial agent.

Requirements:
- Import StateGraph, END from langgraph.graph
- Import AgentState from .state
- Import analyze_node, retrieve_node, generate_node, should_continue from .nodes
- Build graph:
  - Add nodes: "analyze", "retrieve", "generate"
  - Set entry point: "analyze"
  - Add conditional edge from "analyze" using should_continue → {"retrieve": "retrieve", "generate": "generate", END: END}
  - Add edge: "retrieve" → "generate"
  - Add conditional edge from "generate" using should_continue → {END: END, "retrieve": "retrieve"}
- Compile and export as `agent_graph = graph.compile()`
- Export `run_agent(query: str) -> str` function that invokes the graph with initial state and returns final_answer
P2-D: 集成 Agent 到 API


Update `src/api/main.py` to integrate the router and agent.

Current file has: GET /, GET /health, GET /test-weaviate, POST /chat (placeholder).

Update POST /chat:
- Request body: `{"query": str}`
- Import IntentRouter from src.router, run_agent from src.agent.graph, KeywordSearcher from src.retrieval.keyword_search
- Initialize router and searcher at module level
- In /chat handler:
  - Call router.route(query) → query_type
  - If SIMPLE: call searcher.search(query), return {"answer": result["result"], "query_type": "simple", "source": "keyword_search"}
  - If COMPLEX: call run_agent(query), return {"answer": answer, "query_type": "complex", "source": "agent"}
- Add error handling: return {"answer": f"Error: {str(e)}", "query_type": "error"}
Phase 3 — Weaviate 混合检索
P3-A: Weaviate 客户端 + Schema


Create `src/retrieval/weaviate_client.py` for a financial RAG system using weaviate-client v3.

Requirements:
- `get_client() -> weaviate.Client`: singleton, connects to WEAVIATE_URL env (default http://localhost:8080), passes OPENAI_API_KEY as X-OpenAI-Api-Key header
- `create_schema(client)`: create class "FinancialDocument" if not exists, with properties:
  - title (text), content (text), doc_type (text), ticker (text), date (text)
  - vectorizer: text2vec-openai
- `schema_exists(client) -> bool`: check if FinancialDocument class exists

Create `src/retrieval/schemas.py`:
- Dataclass `FinancialDocument` with fields: title, content, doc_type, ticker, date
P3-B: 数据加载脚本


Create `scripts/load_data.py` to load sample financial documents into Weaviate.

Requirements:
- Import get_client, create_schema from src.retrieval.weaviate_client
- Define SAMPLE_DOCS list with 5 realistic financial documents (dicts with title, content, doc_type, ticker, date):
  - 2 earnings report excerpts (TSLA, NVDA)
  - 2 financial news items
  - 1 analyst report
- create_schema if not exists
- Batch import documents using client.batch.configure(batch_size=10)
- Print progress and final count

Run with: `python scripts/load_data.py`
P3-C: 混合检索实现


Create `src/retrieval/hybrid_search.py` for Weaviate hybrid search.

Requirements:
- `vector_search(client, query: str, limit: int = 5) -> list[dict]`: use nearText with concepts=[query], return list of {title, content, doc_type, ticker, certainty}
- `bm25_search(client, query: str, limit: int = 5) -> list[dict]`: use bm25 with query=query, return same format
- `hybrid_search(client, query: str, alpha: float = 0.5, limit: int = 5) -> list[dict]`: use Weaviate hybrid search with alpha parameter (0=BM25, 1=vector), deduplicate results by title, return merged list

Update `src/retrieval/__init__.py` to export hybrid_search.
Phase 4 — 工具调用
P4-A: 工具定义


Create the following LangChain tools for a financial agent:

1. `src/tools/stock_price.py`:
   - @tool `get_stock_price(ticker: str) -> str`
   - Use yfinance: yf.Ticker(ticker).history(period="1d")
   - Return f"{ticker} current price: ${price:.2f}, change: {change:+.2f}%"
   - Handle exceptions, return error message

2. `src/tools/portfolio.py`:
   - @tool `get_portfolio() -> str`
   - Return hardcoded mock portfolio as formatted string:
     TSLA: 50 shares @ $245.30, NVDA: 30 shares @ $875.20, AAPL: 100 shares @ $189.50
   - Include total value calculation

3. `src/tools/__init__.py`: export all_tools = [get_stock_price, get_portfolio]
P4-B: Tool Node 集成到 Agent


Update `src/agent/nodes.py` and `src/agent/graph.py` to add tool calling.

In nodes.py:
- Import all_tools from src.tools
- Update analyze_node: bind tools to LLM using llm.bind_tools(all_tools), if response has tool_calls set intent="tool_call" and store tool_calls in state
- Add `tool_node(state)`: execute tool calls from state["tool_calls"] using ToolExecutor or manual dispatch, append results to state["messages"], set intent="generate"

In graph.py:
- Add "tool" node using tool_node
- Update should_continue: add "tool_call" → "tool" mapping
- Add edge: "tool" → "generate"
Phase 6 — 前端完善
P6-A: Streamlit 聊天界面


Create `frontend/streamlit_app.py` as a Streamlit chat interface for a financial RAG system.

Requirements:
- Page config: title="Financial Agentic RAG", layout="wide"
- Sidebar: show system status (GET http://backend:8000/health), show query type legend
- Main area: st.chat_message style conversation UI
- Use st.session_state["messages"] to store history
- On user input: POST to http://backend:8000/chat with {"query": user_input}
- Display response with source badge: "简单查询" (green) or "Agent分析" (blue)
- Show spinner while waiting for response
- Handle connection errors gracefully

BACKEND_URL from env var (default http://backend:8000).
这些 prompt 每个都完全独立，可以直接粘贴给 Claude 执行，无需额外上下文。建议执行顺序：P0-A → P0-B → P1-A → P1-B → P2-A → P2-B → P2-C → P2-D，完成后验证端到端流程，再继续 Phase 3+。