import json
import os

# ==========================================
# 1. 定义具体干活的函数
# ==========================================

# 🌟 新知识点：类型提示 (Type Hints)
# city: str 表示参数必须是字符串
# -> str 表示这个函数返回的一定是字符串
def get_weather(city: str) -> str:
    """
    查询天气的工具函数。
    这里为了演示架构，使用模拟数据。你可以随时把它替换成 Day 3 的真实 API 代码。
    """
    print(f"🔍 [工具调用] 正在查询 {city} 的天气...")
    
    # 模拟数据
    mock_data = {
        "city": city,
        "temperature": "25℃", 
        "condition": "晴朗",
        "suggestion": "适合出门写代码"
    }
    return json.dumps(mock_data, ensure_ascii=False)

def save_to_file(filename: str, content: str) -> str:
    """
    保存文件的工具函数。
    """
    print(f"💾 [工具调用] 正在写入文件: {filename}...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"status": "success", "message": f"文件 {filename} 保存成功"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def calculate_sum(a: int, b: int) -> str:
    """
    加法函数。
    """
    print(f"💾 [工具调用] 正在计算{a} + {b} ...")

    result = a+b
    return json.dumps({"result": result})


# ==========================================
# 2. 定义给 AI 看的“说明书” (Schema)
# ==========================================
# 以前这些 JSON 是写在 main.py 里的，现在挪到这里，main.py 就干净了
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "当用户询问天气时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_file",
            "description": "当用户要求保存内容或写文件时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "文件名，必须包含扩展名"},
                    "content": {"type": "string", "description": "要写入的文件内容"}
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "当用户想要计算加法时调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个加数"},
                    "b": {"type": "integer", "description": "第二个加数"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# ==========================================
# 3. 定义工具映射表 (Mapping)
# ==========================================
# 🌟 这行代码很关键！
# 它的作用是：当 AI 说 "我要调用 get_weather" 时，
# 程序能通过这个字典，找到上面定义的 get_weather 函数。
tools_map = {
    "get_weather": get_weather,
    "save_to_file": save_to_file,
    "calculate_sum": calculate_sum
}