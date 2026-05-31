def explain_mcp_topic(topic: str, level: str) -> str:
    return f"""
请用 {level} 水平讲解 MCP 主题：{topic}

要求：

1. 先用一句话说明它是什么
2. 再说明它在 MCP 架构中的作用
3. 给一个简单示例
4. 最后列出学习时最容易混淆的点
"""


def generate_mcp_study_plan(level: str, days: int) -> str:
    return f"""
请为 {level} 水平的学习者生成一个 {days} 天 MCP 学习计划。

要求：

1. 每天包含学习目标
2. 每天包含一个小练习
3. 每天说明验收标准
4. 覆盖 Tool、Resource、Resource Template、Prompt 和 transport
"""


def review_mcp_code(code: str) -> str:
    return f"""
请审查下面这段 MCP 代码。

重点检查：

1. 装饰器是否正确
2. 函数名、参数和返回值是否清晰
3. 类型注解是否完整
4. docstring 是否能帮助 Host 理解能力
5. 是否有 stdio 输出、导入路径或序列化风险

代码：

```python
{code}
```
"""


def debug_mcp_error(error: str) -> str:
    return f"""
请诊断下面这个 MCP 错误。

要求：

1. 判断最可能的问题类型
2. 给出排查顺序
3. 说明每一步要看什么现象
4. 给出最小修复建议

错误：

{error}
"""


def summarize_mcp_concept(topic: str) -> str:
    return f"""
请总结 MCP 概念：{topic}

输出格式：

1. 一句话定义
2. 核心作用
3. 和相邻概念的区别
4. 一个最小示例
5. 学习检查问题
"""


__all__ = [
    "debug_mcp_error",
    "explain_mcp_topic",
    "generate_mcp_study_plan",
    "review_mcp_code",
    "summarize_mcp_concept",
]
