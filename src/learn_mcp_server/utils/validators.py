"""普通 Python 调用与 MCP 调用共用的业务输入校验。"""

import re
from collections.abc import Collection
from ipaddress import ip_address
from urllib.parse import urlsplit


def normalize_key(value: str) -> str:
    """去除首尾空白并转小写，用于教材主题查找。"""
    return value.strip().lower()


def require_not_blank(value: str, field_name: str) -> str:
    """验证非空字符串并返回去除首尾空白的值。"""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} 必须是字符串。")
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} 不能为空。")
    return normalized_value


def require_string_list(value: object, field_name: str) -> list[str]:
    """验证每项都是字符串的列表，否则给出字段错误。"""
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field_name} 必须是字符串列表。")
    return value


def require_choice(value: str, field_name: str, choices: Collection[str]) -> str:
    """标准化有限选项；未知选项不静默替换。"""
    normalized = normalize_key(require_not_blank(value, field_name))
    if normalized not in choices:
        raise ValueError(f"{field_name} 不支持：{value}。可用值：{', '.join(choices)}。")
    return normalized


def require_days(value: int) -> int:
    """本项目学习计划限定 1–30 天；不是 MCP 协议限制。"""
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 30:
        raise ValueError("days 必须是 1–30 之间的整数。")
    return value


def require_http_url(value: str, field_name: str = "server_url") -> str:
    """只校验 HTTP 地址格式，不连接目标；凭证应放在 Host 凭证配置中。"""
    normalized = require_not_blank(value, field_name)
    try:
        parsed = urlsplit(normalized)
        valid = (
            parsed.scheme in {"http", "https"}
            and _valid_hostname(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and "#" not in normalized
            and (parsed.port is None or 1 <= parsed.port <= 65535)
            and not any(
                character.isspace() or ord(character) < 32 or 127 <= ord(character) <= 159
                for character in normalized
            )
            and "\\" not in normalized
            and not parsed.netloc.endswith(":")
        )
    except ValueError:
        valid = False
    if not valid:
        raise ValueError(
            f"{field_name} 必须是有效的 http/https URL，包含主机，且不含内嵌凭证或 fragment。"
        )
    return normalized


def _valid_hostname(hostname: str | None) -> bool:
    if not hostname:
        return False
    try:
        ip_address(hostname)
        return True
    except ValueError:
        pass
    try:
        absolute_hostname = hostname[:-1] if hostname.endswith(".") else hostname
        encoded = absolute_hostname.encode("idna").decode("ascii")
    except UnicodeError:
        return False
    return len(encoded) <= 253 and all(
        re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
        for label in encoded.split(".")
    )


__all__ = [
    "normalize_key",
    "require_choice",
    "require_days",
    "require_http_url",
    "require_not_blank",
    "require_string_list",
]
