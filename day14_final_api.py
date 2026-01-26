from fastapi import FastAPI
from pydantic import BaseModel, Field
import config
from openai import OpenAI

# 1. 初始化客户端
client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

app = FastAPI(title="AI 智能翻译官", description="支持多种语言的高性能翻译接口")

# 2. 定义更严谨的输入模型 (Pydantic 进阶)
class TranslationRequest(BaseModel):
    # Field 可以增加描述，甚至限制长度
    text: str = Field(..., example="你好，世界", description="待翻译的原始文本")
    target_lang: str = Field(default="English", example="Spanish", description="目标语言")

@app.post("/translate")
def translate_api(req: TranslationRequest):
    print(f"📡 收到翻译请求: {req.text} -> {req.target_lang}")

    # 3. 设定翻译官专用的 System Prompt
    system_instruction = f"""
    你是一个专业的同声传译。
    你的任务是将用户输入的文本准确、地道地翻译成 {req.target_lang}。
    注意：
    1. 只输出翻译结果，不要有任何多余的解释。
    2. 保持原有的语气和口吻。
    """

    try:
        response = client.chat.completions.create(
            model=config.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": req.text}
            ],
            temperature=0.3 # 翻译需要严谨，所以降低随机性
        )
        
        result = response.choices[0].message.content
        return {
            "original_text": req.text,
            "translated_text": result,
            "target_language": req.target_lang
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 服务正在启动...")
    print("📱 请在局域网内访问: http://192.168.31.249:8000/docs")
    # host="0.0.0.0" 是关键！它允许局域网内的其他设备（手机）连接
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 运行提示: uvicorn day14_final_api:app --reload

#翻译官系统完结！