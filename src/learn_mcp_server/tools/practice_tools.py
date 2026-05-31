from learn_mcp_server.data.practices import PRACTICE_TASKS
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def generate_learning_plan(level: str) -> str:
    """
    根据学习水平生成 MCP 学习计划。
    """
    normalized_level = normalize_key(require_not_blank(level, "level"))

    title = {
        "beginner": "MCP 入门学习计划",
        "intermediate": "MCP 进阶学习计划",
        "advanced": "MCP 高级学习计划",
    }.get(normalized_level, "MCP 入门学习计划")

    return f"""
# {title}

第 1 天：理解 Host、Client、Server 的关系。
第 2 天：实现并调用第一个 Tool。
第 3 天：实现静态 Resource，并理解 Resource 和 Tool 的区别。
第 4 天：实现 Resource Template，学习 URI 参数映射。
第 5 天：实现 Prompt，封装可复用任务模板。
第 6 天：使用 Inspector 查看 Tools、Resources、Prompts。
第 7 天：整理测试、配置和常见错误排查方式。
"""


def get_practice_task(topic: str) -> str:
    """
    根据主题生成 MCP 练习任务。
    """
    normalized_topic = normalize_key(require_not_blank(topic, "topic"))

    if normalized_topic not in PRACTICE_TASKS:
        available_topics = format_available_items(list(PRACTICE_TASKS.keys()))
        return f"没有找到练习主题：{topic}\n\n当前支持的练习主题包括：\n\n{available_topics}"

    practice = PRACTICE_TASKS[normalized_topic]
    return f"""
# {practice["title"]}

任务：

{practice["task"]}

完成标准：

1. 函数有清晰的类型注解
2. 函数有 docstring
3. 返回内容可以被 MCP Host 理解
4. 有对应测试覆盖核心行为
"""


def check_answer(topic: str, answer: str) -> str:
    """
    根据主题和用户回答给出学习反馈。
    """
    normalized_topic = normalize_key(require_not_blank(topic, "topic"))
    normalized_answer = normalize_key(require_not_blank(answer, "answer"))

    practice = PRACTICE_TASKS.get(normalized_topic)
    if practice is None:
        available_topics = format_available_items(list(PRACTICE_TASKS.keys()))
        return f"暂时不能检查主题：{topic}\n\n当前支持的主题包括：\n\n{available_topics}"

    matched_keywords = [
        keyword for keyword in practice["keywords"]
        if keyword.lower() in normalized_answer
    ]

    if matched_keywords:
        return f"""
# 答案反馈

答得不错，你的回答已经覆盖了 {practice["title"]} 的关键点。

命中的关键词：{", ".join(matched_keywords)}

可以继续补充：它适合什么场景、如何注册、Host 如何发现和调用它。
"""

    return f"""
# 答案反馈

你的回答还可以继续补充 {practice["title"]} 的核心关键词。

建议至少提到：{", ".join(practice["keywords"])}
"""


def suggest_next_step(current_topic: str) -> str:
    """
    根据当前学习主题推荐下一步。
    """
    normalized_topic = normalize_key(require_not_blank(current_topic, "current_topic"))

    next_steps = {
        "mcp": ("host", "先理解 Host、Client、Server 三个角色。"),
        "host": ("client", "继续看 Client 如何代表 Host 与 MCP Server 通信。"),
        "client": ("server", "继续看 Server 如何暴露能力。"),
        "server": ("tool", "下一步学习 Tool，因为它是最容易直接调用的能力。"),
        "tool": ("resource", "学完 Tool 后，继续学习 Resource，区分动作和上下文。"),
        "resource": ("resource-template", "继续学习 Resource Template，掌握动态 URI。"),
        "resource-template": ("prompt", "继续学习 Prompt，理解可复用任务模板。"),
        "prompt": ("transport", "继续学习 stdio 和 streamable-http 传输方式。"),
        "transport": ("config", "继续学习 Host 配置和本地/远程接入方式。"),
        "stdio": ("streamable-http", "对比本地 stdio 和 HTTP 运行方式。"),
        "streamable-http": ("debug", "继续学习 HTTP 服务调试和配置排查。"),
        "config": ("debug", "继续学习常见错误诊断。"),
        "debug": ("tests", "最后补测试，确认 MCP 能力真的能被 Client 使用。"),
    }

    next_topic, reason = next_steps.get(
        normalized_topic,
        ("tool", "如果不确定当前进度，建议从 Tool 开始验证 MCP 的可调用能力。"),
    )

    return f"""
# 下一步学习建议

当前主题：{normalized_topic}

推荐下一步：{next_topic}

原因：
{reason}

建议操作：
1. 调用 explain_concept("{next_topic}") 查看概念说明。
2. 如果有示例，调用 get_code_example 或 mcp://examples/{{name}} 查看代码。
3. 完成一个小练习后，再调用 check_answer 检查理解是否到位。

后续衔接：
Tool -> Resource -> Resource Template -> Prompt -> Transport -> Config -> Debug
""".strip()


__all__ = ["check_answer", "generate_learning_plan", "get_practice_task", "suggest_next_step"]
