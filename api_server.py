from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
import uvicorn
import config
import traceback
import shutil # 👈 用来保存文件
import os     # 用来创建文件夹
from pdf_loader import load_pdf_to_chroma

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
# ... (之前的代码) ...
print("🚀 正在启动 API 服务器...")
bot = SecuRAG()

# --- 🔥 新增：心跳检测接口 (Heartbeat) ---
# 前端只用 ping 这个接口，不用传任何数据，响应快
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "SecuRAG-API"}

# ... (之后的 chat 接口保持不变) ...

print("✅ 引擎加载完毕，等待请求...")

# 4. 定义请求的数据格式 (Data Model)
# 前端(Streamlit/Postman)发过来的 JSON 必须长这样
class ChatRequest(BaseModel):
    query: str  # 用户的问题
    session_id: str  # 会话 ID
    temperature: float = 0.1
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
        response = bot.chat(user_query, request.session_id, request.temperature)
        
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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    文件上传接口：
    1. 接收前端传来的 PDF
    2. 保存到本地
    3. 调用 RAG 引擎进行切片入库
    """
    try:
        # 1. 确保有个放文件的地方
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"
        
        # 2. 把文件从内存写到硬盘
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"📂 [API] 接收到文件: {file.filename}")
        
        # 3. 呼叫 PDF 加载器 (Day 19 的代码)
        # 这一步会把 PDF 变成向量存进 ChromaDB
        load_pdf_to_chroma(file_path)
        
        return {"status": "success", "filename": file.filename, "msg": "知识库入库成功！"}

    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return {"status": "error", "msg": str(e)}
# 6. 启动入口
if __name__ == "__main__":
    # host="0.0.0.0" 代表允许局域网访问
    # port=8000 是 API 的标准端口
    print("⚡⚡⚡ 我是全新的无斜杠版 API Server！⚡⚡⚡") # 👈 加上这行
    uvicorn.run(app, host="0.0.0.0", port=8000)