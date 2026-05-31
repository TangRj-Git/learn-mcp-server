"""
这三个函数是输入验证工具：
用于确保 MCP Server 接收的参数格式正确。
"""


def normalize_key(value: str) -> str:
    """
    去除首尾空格并转小写，用于标准化键名
    """
    return value.strip().lower()


def require_not_blank(value: str, field_name: str) -> str:
    """
    检查字符串非空，为空则抛出异常
    :param value:
    :param field_name:
    :return:
    """
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} 不能为空。")
    return normalized_value


def require_string_list(value: object, field_name: str) -> list[str]:
    """
    验证对象是否为纯字符串列表，否则抛出异常
    :param value:
    :param field_name:
    :return:
    """
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field_name} 必须是字符串列表。")
    return value


__all__ = ["normalize_key", "require_not_blank", "require_string_list"]
