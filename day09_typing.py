#这是一个学习Type Hints(类型提示)的文件
from typing import List, Dict, Optional, Any
def greeting(name: str, age: int) -> str:
    return f"你好, {name}, 你今年 {age} 岁了。"

# 调用
print(greeting("Alice", 25))

def calculate_average(scores: List[int]) -> float:
    # scores 是一个全是数字的列表
    return sum(scores) / len(scores)#用了/所以必须是小数，//就可以整数

def get_student_info(name: str, scores: List[int]) -> Dict[str, Any]:
    # 返回一个字典，key是字符串，value是任何东西
    return {
        "name": name,
        "average": sum(scores) / len(scores)
    }

def search_db(query: str, limit: Optional[int]=10) ->None:#Optional[int]表内容可为int可为none
    # limit 默认是 10，但也可以传 None
    if limit is None:
        print(f"搜索全部: {query}")
    else:
        print(f"搜索 {query}, 限制 {limit} 条")

# 这是一个处理待办事项(Todo)的函数
# todos 是一个列表，里面装着字典
# owner 是谁的任务 (字符串)
# filter_date 是日期 (字符串)，可能是 None
def process_todos(todos:List[Dict[str,Any]], owner: str, filter_date : Optional[str] = None) -> List[str]:
    result = []
    for item in todos:
        if item["user"] == owner:#在 Python 里，能使用方括号 ["xxx"] 来取值的，只有 字典 (Dictionary)
            # 如果 filter_date 不是 None，还要检查日期
            if filter_date is not None and item["date"] != filter_date:
                continue
            result.append(item["title"])
    return result