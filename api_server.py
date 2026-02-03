from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import config
import traceback


# 1. 引入你的核心引擎
# 这就是"模块化"的好处，我们不需要重写 RAG 逻辑，直接 import 进来！
from securag_engine import SecuRAG

# 2. 初始化 API APP
app = FastAPI(
    title="SecuRAG Core API",
    description="基于本地大模型(Ollama)与RAG技术的安全防御API",
    version="1.0"
)

# 3. 启动引擎 (全局单例模式)
# 这样服务器启动时，模型和数据库只加载一次，不用每次请求都重新加载
print("🚀 正在启动 API 服务器，加载 SecuRAG 引擎...")
bot = SecuRAG()
print("✅ 引擎加载完毕，等待请求...")

# 4. 定义请求的数据格式 (Data Model)
# 前端(Streamlit/Postman)发过来的 JSON 必须长这样
class ChatRequest(BaseModel):
    query: str  # 用户的问题
    session_id: str  # 会话 ID

# 5. 定义接口 (Endpoint)
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    核心聊天接口
    输入: {"query": "AMOGEL模型是什么?"}
    输出: {"answer": "AMOGEL是..."}
    """
    try:
        # 调用核心引擎的 chat 方法
        user_query = request.query
        response = bot.chat(user_query, request.session_id)
        
        # 返回标准的 JSON
        return {
            "status": "success",
            "answer": response,
            "mode": config.APP_MODE # 顺便告诉前端，现在用的是 local 还是 cloud
        }
    
    except Exception as e:
        # 👇 2. 新增：让法医打印尸检报告
        print("❌ API 严重崩溃，错误详情如下：")
        traceback.print_exc() 
        
        # 返回 500 给前端
        raise HTTPException(status_code=500, detail=str(e))

# 6. 启动入口
if __name__ == "__main__":
    # host="0.0.0.0" 代表允许局域网访问
    # port=8000 是 API 的标准端口
    uvicorn.run(app, host="0.0.0.0", port=8000)