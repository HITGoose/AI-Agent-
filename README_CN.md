# 🔬 SecuRAG: 学术研究智能Agent

> 面向学术文献研究的生产级RAG Agent，集成多阶段检索、意图路由和自动化评估。

## 📖 项目介绍

**SecuRAG** 是一个基于完整Agent架构的智能学术研究助手。不同于简单的RAG系统，SecuRAG实现了**多阶段检索流水线**和**自主意图路由器**，能自主判断是检索知识库还是直接回答。

### 核心功能

* **意图路由器**：自主将用户查询分类为SEARCH或CHAT，20条测试集准确率达85%
* **混合检索**：BM25关键词检索+稠密向量检索双路召回，提升召回率
* **Reranking重排**：CrossEncoder二阶段精排，提升检索精度
* **查询重写**：基于LLM的指代消解，处理多轮对话中的模糊查询
* **多轮记忆**：基于Session ID的对话历史管理
* **LLM-as-a-Judge**：自动评估回答的相关性和完整性
* **本地隐私模式**：基于Ollama+ChromaDB完全离线运行，数据零出网
* **微服务架构**：FastAPI后端+Streamlit前端解耦，支持Docker一键部署

---

## 📊 性能指标

| 指标 | 结果 |
|------|------|
| 意图路由准确率 | 85% (17/20测试用例) |
| 检索方式 | BM25+向量混合，Top-5召回 |
| 重排模型 | CrossEncoder ms-marco-MiniLM-L-6-v2 |
| 评估方式 | LLM-as-a-Judge（相关性+完整性） |

---

## 🚀 安装与运行

### 环境要求
- Python 3.10+
- 安装并运行Ollama
- Docker（可选）

### 1. 克隆并安装依赖

git clone https://github.com/HITGoose/SecuRAG-Agent.git
cd SecuRAG-Agent
pip install -r requirements.txt

### 2. 配置环境变量

APP_MODE=local
OLLAMA_HOST=http://localhost:11434
DEEPSEEK_API_KEY=你的key（云端模式需要）

### 3. 拉取本地模型

ollama pull deepseek-r1:1.5b

### 4. 启动服务

方式A：Docker一键启动
docker-compose up

方式B：手动启动
终端1：python api_server.py
终端2：streamlit run frontend.py

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 大模型 | DeepSeek / Ollama |
| 向量数据库 | ChromaDB |
| 检索 | BM25 + 稠密向量混合 |
| 重排 | CrossEncoder |
| 后端 | FastAPI |
| 前端 | Streamlit |
| 部署 | Docker |

---

## 📁 项目结构

securag_engine.py    - 核心RAG Agent引擎
hybrid_retriever.py  - BM25+向量混合检索
reranker.py          - CrossEncoder重排
security_guard.py    - 输入清洗
pdf_loader.py        - PDF入库流水线
api_server.py        - FastAPI后端
frontend.py          - Streamlit界面
test_intent.py       - 意图路由评估
test_eval.py         - LLM评估
Dockerfile
docker-compose.yml
