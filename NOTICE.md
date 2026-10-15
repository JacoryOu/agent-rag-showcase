# 来源与第三方组件说明

当前仓库发布的是新整理的项目说明、合成演示资料、真实运行截图及材料校验脚本，不包含原业务源码或第三方源码。文档整理与校验工具使用AI辅助；个人贡献边界见[contributions.md](docs/contributions.md)。未核实的源码许可不会通过本NOTICE或新增总括许可证被重新授权。本仓库未授予一个覆盖原完整项目/第三方代码的统一开源许可。

## 原应用实际依赖

版本来自本地安装元数据/已有依赖记录，是运行环境快照而非本仓库的安装合同。没有复制依赖源码或模型权重；请遵循各项目自身版权、许可证和模型服务条款。

| 组件 | 已记录版本 | 在原应用中的职责/来源 |
|---|---|---|
| Python | 3.13.9 | 运行时；[python.org](https://www.python.org/) |
| FastAPI / Uvicorn | 0.140.13 / 0.51.0 | HTTP/ASGI；[FastAPI](https://github.com/fastapi/fastapi)、[Uvicorn](https://github.com/Kludex/uvicorn) |
| LangChain / LangGraph | 1.3.14 / 1.2.9 | Agent/工具与固定图；[LangChain](https://github.com/langchain-ai/langchain)、[LangGraph](https://github.com/langchain-ai/langgraph) |
| LlamaIndex-core | 0.14.23 | 文档/分块/检索适配；[LlamaIndex](https://github.com/run-llama/llama_index) |
| Chroma | 1.5.9 | 本地向量持久化；[Chroma](https://github.com/chroma-core/chroma) |
| FlagEmbedding | 1.4.2 | 本地重排；[FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) |
| ChatQwen / OpenAI SDK / HTTPX | langchain-qwq 0.3.5 / 2.48.0 / 0.28.1 | 兼容模型传输；[langchain-qwq](https://pypi.org/project/langchain-qwq/)、[OpenAI SDK](https://github.com/openai/openai-python)、[HTTPX](https://github.com/encode/httpx) |
| psycopg / psycopg-pool | 3.3.4 / 3.3.1 | PostgreSQL异步连接；[Psycopg](https://github.com/psycopg/psycopg) |
| PyJWT | 2.15.1 | JWT验证；[PyJWT](https://github.com/jpadilla/pyjwt) |
| React / Vite / TypeScript | 19.3.0 / 8.3.0 / 5.9.3 | 前端；[React](https://github.com/facebook/react)、[Vite](https://github.com/vitejs/vite)、[TypeScript](https://github.com/microsoft/TypeScript) |

组件原生功能不当作项目作者自行实现的框架内核。具体本地模型名称/权重路径、连接地址与凭据不公开；模型权重公开与商用条件需独立核查。
