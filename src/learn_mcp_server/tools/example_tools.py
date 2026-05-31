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
    lines.append("可以继续调用 get_code_example(topic) 查看某个示例的完整代码。")
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

    return f"""
# {normalized_name} 示例说明

{CODE_EXAMPLES[normalized_name].strip()}

## 说明

这个示例展示了 {normalized_name} 在 FastMCP 中的基本写法。
其中装饰器负责把普通 Python 函数注册到 MCP Server，函数名、参数类型和 docstring 会帮助 Host 理解这个能力。
"""


__all__ = ["explain_code_example", "get_code_example", "list_code_examples"]
