# 尝试简单模块化 AI Agent

### 📊 Day 7 成果总结

**项目名称**: 模块化重构 - 将单文件 Agent 拆分为多文件项目结构

**核心学习内容**:

- ✅ **项目模块化架构**:
  - `main.py`: 主程序入口，负责聊天循环和工具调用协调逻辑
  - `tools.py`: 工具函数库，包含函数定义、Schema 描述和工具映射表
  - `config.py`: 配置管理模块，统一管理 API Key、模型参数和系统提示词

- ✅ **Python 模块导入**:
  - 掌握了 `import config` 和 `import tools` 的模块导入方式
  - 理解了模块化带来的代码组织和可维护性提升

- ✅ **环境变量管理**:
  - 使用 `python-dotenv` 库加载 `.env` 文件
  - 通过 `os.getenv()` 安全地读取敏感配置（API Key）
  - 学会了将配置与代码分离的最佳实践

- ✅ **代码组织原则**:
  - **关注点分离**: 配置、工具、主逻辑各司其职
  - **可扩展性**: 新增工具只需在 `tools.py` 中添加，无需修改主程序
  - **可维护性**: 修改配置只需改 `config.py`，代码结构清晰

**技术亮点**:

- 实现了**三层架构**: 配置层 (`config.py`) → 工具层 (`tools.py`) → 应用层 (`main.py`)
- 掌握了**工具映射表 (tools_map)** 的设计模式，实现了函数名到函数对象的动态映射
- 理解了**Type Hints (类型提示)** 的实际应用：`def get_weather(city: str) -> str:`
- 学会了**常量命名规范**：使用大写字母表示配置常量（如 `MODEL_NAME`, `TEMPERATURE`）

**代码质量提升**:

- 从单文件脚本升级为**多文件项目结构**，符合生产环境标准
- 代码职责清晰，每个文件都有明确的职责边界
- 添加了详细的注释，解释了模块化设计的思路

**项目结构**:

```
ai_agent_project/
├── main.py      # 主程序：聊天循环 + 工具调用协调
├── tools.py     # 工具库：函数定义 + Schema + 映射表
├── config.py    # 配置管理：API Key + 模型参数
└── .env         # 环境变量（敏感信息）
```

**下一步方向** (Day 8):
- 🧘 缓冲日：复盘 Day 1-7 的学习成果
- 开始 LeetCode "两数之和"，熟悉 Python 基础数据结构操作

### 📊 Day 9 成果总结
**项目名称**: `day09_typing.py` - Type Hints (类型提示) 实战练习

**核心学习内容**:
- ✅ **基础类型提示**:
  - 参数类型：`name: str`, `age: int`
  - 返回值类型：`-> str`, `-> float`, `-> None`
  - 理解了类型提示的基本语法：`参数名: 类型`, `-> 返回类型`
- ✅ **集合类型提示**:
  - `List[int]`: 整数列表类型
  - `Dict[str, Any]`: 字典类型（键为字符串，值为任意类型）
  - 掌握了 `typing` 模块的导入：`from typing import List, Dict, Optional, Any`
- ✅ **Optional 类型 (可选类型)**:
  - `Optional[int]`: 可以是 int 或 None
  - `Optional[str] = None`: 默认值为 None 的可选字符串参数
  - 理解了可选参数的实际应用场景（如默认参数、过滤条件）
- ✅ **复杂嵌套类型**:
  - `List[Dict[str, Any]]`: 列表中的每个元素都是字典
  - 掌握了多层嵌套类型的表示方法
- ✅ **实际应用场景**:
  - 学生信息处理：`get_student_info(name: str, scores: List[int]) -> Dict[str, Any]`
  - 待办事项过滤：`process_todos(todos: List[Dict[str, Any]], ...) -> List[str]`
  - 数据库查询：`search_db(query: str, limit: Optional[int] = 10) -> None`

**技术亮点**:
- 理解了**类型提示的作用**：提高代码可读性，帮助 IDE 智能提示，提前发现类型错误
- 掌握了**集合类型的表示方法**：用 `List[...]` 和 `Dict[...]` 表示复杂数据结构
- 学会了**Optional 的使用场景**：处理可能为 None 的参数和返回值
- 理解了**Python 与静态类型语言的区别**：类型提示是"提示"而非强制，运行时不会检查

**代码质量提升**:
- 代码可读性大幅提升：通过类型提示，一眼就能看出函数需要什么参数、返回什么类型
- 为后续学习 Pydantic（Day 10）打下基础：Pydantic 会利用类型提示进行数据验证
- 符合现代 Python 开发规范：Python 3.5+ 推荐使用类型提示

**关键概念掌握**:
- **`/` vs `//` 的区别**：`/` 返回浮点数，`//` 返回整数（在 `calculate_average` 函数中的理解）
- **字典访问方式**：使用方括号 `item["key"]` 访问字典值
- **类型提示的层次**：从简单类型 (`str`, `int`) → 集合类型 (`List`, `Dict`) → 可选类型 (`Optional`)