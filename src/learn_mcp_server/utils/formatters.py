"""教材主题列表的单行与 Markdown 格式。"""


def format_available_items(items: list[str]) -> str:
    """用逗号连接简短的主题名称。"""
    return ", ".join(items)


def format_markdown_list(items: list[str]) -> str:
    """每个主题输出一行 Markdown 列表项。"""
    return "\n".join(f"- {item}" for item in items)


__all__ = ["format_available_items", "format_markdown_list"]
