from pydantic import BaseModel, ValidationError
from typing import List, Optional

# 1. 定义“模具” (Schema)
class User(BaseModel):
    name: str
    age: int
    hobbies: List[str] = [] # 默认是空列表
    email: Optional[str] = None # 可选字段

# 2. 测试数据 (注意：age 我故意写成了字符串 "18")
external_data = {
    "age": "18", 
    "hobbies": ["coding", "reading"]
}

try:
    # 3. 实例化 (自动安检 + 自动类型转换)
    user = User(**external_data) # ** 是解包字典
    print(f"✅ 成功创建用户: {user.name}")
    print(f"   年龄类型: {type(user.age)}") # 竟然自动变成了 <class 'int'> !
    print(f"   数据概览: {user.model_dump()}") # 打印成字典

except ValidationError as e:
    print(f"❌ 数据校验失败: {e}")

# ==============
# 🎯 你的小作业：
# 请尝试把上面的 external_data 改乱：
# 1. 把 "age" 改成 "not_a_number" (看报错)
# 2. 把 "name" 删掉 (看报错)
# ==============