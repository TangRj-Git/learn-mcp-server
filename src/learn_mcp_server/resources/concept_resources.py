from learn_mcp_server.data.concepts import CONCEPTS
from learn_mcp_server.data.references import BASELINE, reference_note
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def _document(name: str, title: str) -> str:
    return f"# {title}\n\n{CONCEPTS[name].strip()}{reference_note(name)}"


def get_docs_introduction() -> str:
    return _document("mcp", "MCP 简介")


def get_docs_tools() -> str:
    return _document("tool", "MCP Tool")


def get_docs_resources() -> str:
    return (
        _document("resource", "MCP Resource")
        + "\n\n注册：@mcp.resource(uri)，同时声明 MIME 与 description。"
    )


def get_docs_prompts() -> str:
    return _document("prompt", "MCP Prompt")


def get_docs_transports() -> str:
    return _document("transport", "MCP Transport")


def get_docs_architecture() -> str:
    return (
        f"# MCP 架构\n\n{BASELINE}\n\nHost 管理模型与用户交互 → Client 处理协议 → Server 暴露能力。\n\nFastMCP 管理通信，registry 显式注册，tools/resources/prompts 使用内置 data。\n\n"
        + CONCEPTS["server"].strip()
    )


def get_docs_host_client_server() -> str:
    return "# Host、Client、Server\n\n" + "\n\n".join(
        CONCEPTS[name].strip() + reference_note(name) for name in ("host", "client", "server")
    )


def get_docs_concepts() -> str:
    return (
        "# MCP 概念总览\n\nTool / Resource / Prompt 与协议、传输、工程实践。\n\n"
        + BASELINE
        + "\n\n"
        + "\n".join(
            f"- {name}：通过 mcp://concepts/{name} 读取正文、版本与出处。" for name in CONCEPTS
        )
    )


def get_docs_resource_template() -> str:
    return _document("resource-template", "MCP Resource Template")


def get_docs_stdio() -> str:
    return _document("stdio", "stdio")


def get_docs_streamable_http() -> str:
    return _document("streamable-http", "streamable-http")


def get_docs_json_rpc() -> str:
    return _document("json-rpc", "JSON-RPC")


def get_docs_lifecycle() -> str:
    return _document("lifecycle", "MCP 生命周期")


def get_docs_elicitation() -> str:
    return _document("elicitation", "MCP Elicitation")


def get_docs_authorization() -> str:
    return _document("authorization", "MCP Authorization")


def get_docs_security() -> str:
    return _document("security", "MCP Security")


def get_docs_tasks() -> str:
    return _document("tasks", "MCP Tasks")


def get_concept_resource(name: str) -> str:
    """读取概念的正文、适用版本与官方出处；未知名称返回帮助页。"""
    normalized = normalize_key(require_not_blank(name, "name"))
    if normalized not in CONCEPTS:
        return f"没有找到概念：{name}\n\n当前支持的概念包括：\n\n{format_available_items(list(CONCEPTS))}\n\n这是帮助页，不是该未知主题的正文。"
    return _document(normalized, normalized)


__all__ = [
    "get_concept_resource",
    "get_docs_architecture",
    "get_docs_authorization",
    "get_docs_concepts",
    "get_docs_elicitation",
    "get_docs_host_client_server",
    "get_docs_introduction",
    "get_docs_json_rpc",
    "get_docs_lifecycle",
    "get_docs_prompts",
    "get_docs_resource_template",
    "get_docs_resources",
    "get_docs_security",
    "get_docs_stdio",
    "get_docs_streamable_http",
    "get_docs_tasks",
    "get_docs_tools",
    "get_docs_transports",
]
