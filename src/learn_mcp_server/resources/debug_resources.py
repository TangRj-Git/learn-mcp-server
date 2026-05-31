from learn_mcp_server.data.configs import DEBUG_GUIDES
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def get_debug_common_errors() -> str:
    return DEBUG_GUIDES["common-errors"].strip()


def get_debug_stdio_errors() -> str:
    return DEBUG_GUIDES["stdio-errors"].strip()


def get_debug_http_errors() -> str:
    return DEBUG_GUIDES["http-errors"].strip()


def get_debug_config_errors() -> str:
    return DEBUG_GUIDES["config-errors"].strip()


def get_debug_resource(error_type: str) -> str:
    normalized_error_type = normalize_key(require_not_blank(error_type, "error_type"))

    if normalized_error_type not in DEBUG_GUIDES:
        available_guides = format_available_items(list(DEBUG_GUIDES.keys()))
        return f"没有找到调试文档：{error_type}\n\n当前支持的调试文档包括：\n\n{available_guides}"

    return DEBUG_GUIDES[normalized_error_type].strip()


__all__ = [
    "get_debug_common_errors",
    "get_debug_config_errors",
    "get_debug_http_errors",
    "get_debug_resource",
    "get_debug_stdio_errors",
]
