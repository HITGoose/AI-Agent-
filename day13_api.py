from fastapi import FastAPI
from pydantic import BaseModel
from main import chat_loop  # ❌ 暂时别直接导 main，可能会死循环，我们稍后手动搬逻辑
# 正确做法：导入工具和配置
import config
from tools import tools_map, tools_schema
from openai import OpenAI
import json

app = FastAPI()

# 1. 定义请求的数据格式 (Pydantic 立功了！)
class UserQuery(BaseModel):
    query: str

# 2. 初始化客户端 (搬运之前的代码)
client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

@app.post("/chat")  # 注意这里变成了 POST，因为我们要发数据给服务器
def chat_endpoint(user_input: UserQuery):
    print(f"📩 收到用户请求: {user_input.query}")
    
    # 1. 构造消息列表 (System Prompt + 用户输入)
    messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT},
        {"role": "user", "content": user_input.query}
    ]

    # 2. 调用 LLM (还是熟悉的配方)
    # 注意：为了 API 响应速度，这里我们暂时不加 Tool Calling 的复杂循环，先测试对话
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=messages,
        temperature=0.7
    )

    # 3. 提取 AI 的回答
    ai_content = response.choices[0].message.content
    
    # 4. 返回给用户
    return {
        "user": user_input.query,
        "ai_response": ai_content
    }
