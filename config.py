import os
from dotenv import load_dotenv

#强制加载 .env 文件
load_dotenv()

#获取 Key
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"

#定义一些常量 (用大写字母表示常量，这是规范)
MODEL_NAME = "deepseek-chat"
TEMPERATURE = 1.3 
MAX_TOKENS = 1000

#AI人设
SYSTEM_PROMPT = """
你是一个全能的 Python 助手。
你的性格是幽默、风趣的。
如果用户问天气，请使用 get_weather 工具。
如果用户让你保存文件，请使用 save_to_file 工具。
"""