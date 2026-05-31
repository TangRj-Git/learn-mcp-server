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
    """
    这个函数根据名称获取配置文档资源：
    验证输入：标准化名称（去空格、转小写），确保非空
    查找文档：如果名称不在 CONFIG_DOCS 字典中，返回错误提示和可用配置列表
    返回结果：找到则返回对应的配置文档内容（已去除首尾空白）
    用于动态提供 MCP Server 配置相关的说明文档。
    :param name:
    :return:
    """
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
