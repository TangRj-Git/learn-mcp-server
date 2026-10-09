"""代码示例查询；完整实现来自包内 demo.py。"""

from learn_mcp_server.data.examples import CODE_EXAMPLES
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def list_code_examples() -> str:
    """
    列出当前内置的 MCP 示例代码主题。
    """
    lines = ["# MCP 示例清单", ""]

    for index, example_name in enumerate(CODE_EXAMPLES.keys(), start=1):
        lines.append(f"{index}. {example_name}")

    lines.append("")
    lines.append(
        "调用 get_code_example(topic) 查看示例；minimal-server 是完整入口，其余主题包含片段或 Client。"
    )
    return "\n".join(lines)


def get_code_example(topic: str) -> str:
    """
    根据主题名称获取 MCP 示例代码。
    """
    normalized_topic = normalize_key(require_not_blank(topic, "topic"))

    if normalized_topic not in CODE_EXAMPLES:
        available_examples = format_available_items(list(CODE_EXAMPLES.keys()))
        return f"没有找到示例：{topic}\n\n当前支持的示例包括：\n\n{available_examples}"

    return CODE_EXAMPLES[normalized_topic].strip()


def explain_code_example(example_name: str) -> str:
    """
    解释一个 MCP 示例代码的作用。
    """
    normalized_name = normalize_key(require_not_blank(example_name, "example_name"))

    if normalized_name not in CODE_EXAMPLES:
        available_examples = format_available_items(list(CODE_EXAMPLES.keys()))
        return f"没有找到示例：{example_name}\n\n当前支持的示例包括：\n\n{available_examples}"

    focus = (
        "沿着能力发现、Tool 调用、Resource 读取和 Prompt 获取阅读。Client(mcp) 是内存连接，真实传输见 transport_client.py。"
        if normalized_name == "end-to-end-client"
        else "先看函数签名、类型和 docstring，再看装饰器的注册元数据；通过 Client 检查实际结果与失败行为。片段所需 import 和入口见 minimal-server。"
    )
    return f"{CODE_EXAMPLES[normalized_name].strip()}\n\n## 阅读重点\n\n{focus}"


__all__ = ["explain_code_example", "get_code_example", "list_code_examples"]
