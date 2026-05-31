"""
这两个函数是简单的字符串格式化工具：
它们帮助 MCP Server 以一致且美观的方式呈现列表数据，提升用户体验！
"""


def format_available_items(items: list[str]) -> str:
    """
    紧凑的单行格式，适合简短列举
    :param items:
    :return:
    """
    return ", ".join(items)


def format_markdown_list(items: list[str]) -> str:
    """
    清晰的多行格式，适合文档展示
    :param items:
    :return:
    """
    return "\n".join(f"- {item}" for item in items)


__all__ = ["format_available_items", "format_markdown_list"]
