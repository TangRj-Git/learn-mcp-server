"""配置资料读取；不执行配置中的命令，也不连接 URL。"""

from learn_mcp_server.data.configs import CONFIG_DOCS
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def get_docs_config_stdio() -> str:
    return CONFIG_DOCS["stdio"].strip()


def get_docs_config_http() -> str:
    return CONFIG_DOCS["streamable-http"].strip()


def get_docs_config_local_vs_remote() -> str:
    return CONFIG_DOCS["local-vs-remote"].strip()


def get_docs_config_common_errors() -> str:
    return CONFIG_DOCS["common-errors"].strip()


def get_config_resource(name: str) -> str:
    """按标准化名称读取配置说明；未知名称返回可用主题。"""
    normalized_name = normalize_key(require_not_blank(name, "name"))

    if normalized_name not in CONFIG_DOCS:
        available_configs = format_available_items(list(CONFIG_DOCS.keys()))
        return f"没有找到配置文档：{name}\n\n当前支持的配置文档包括：\n\n{available_configs}"

    return CONFIG_DOCS[normalized_name].strip()


__all__ = [
    "get_config_resource",
    "get_docs_config_common_errors",
    "get_docs_config_http",
    "get_docs_config_local_vs_remote",
    "get_docs_config_stdio",
]
