from learn_mcp_server.data.concepts import CONCEPTS
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def get_docs_introduction() -> str:
    return """
# MCP 简介

MCP，全称是 Model Context Protocol，中文可以理解为模型上下文协议。

它的目标是让大模型应用用统一方式连接外部工具、数据资源和提示词模板。
"""


def get_docs_tools() -> str:
    return """
# MCP Tool

Tool 是 MCP Server 暴露给模型调用的可执行能力。

在 FastMCP 中，可以使用 @mcp.tool() 把一个 Python 函数注册成 Tool。
"""


def get_docs_resources() -> str:
    return """
# MCP Resource

Resource 是 MCP Server 暴露出来的可读取上下文内容。

在 FastMCP 中，可以使用 @mcp.resource() 把一个函数注册成 Resource。
"""


def get_docs_prompts() -> str:
    return """
# MCP Prompt

Prompt 是 MCP Server 提供的可复用提示词模板。

在 FastMCP 中，可以使用 @mcp.prompt() 注册 Prompt。
"""


def get_docs_transports() -> str:
    return """
# MCP Transport

Transport 是 MCP Client 和 MCP Server 之间传递 MCP 消息的方式。

常见方式包括 stdio 和 streamable-http。
"""


def get_docs_architecture() -> str:
    return """
# MCP 架构

MCP 架构通常由 Host、Client、Server 三层组成。
"""


def get_docs_host_client_server() -> str:
    return """
# Host、Client、Server

Host 是用户使用的应用，Client 是 Host 内部负责 MCP 协议通信的组件，Server 是暴露能力的服务端。
"""


def get_docs_concepts() -> str:
    return """
# MCP 概念总览

MCP 学习可以先抓住这些核心概念：

1. Host：用户直接使用的大模型应用
2. Client：Host 内部负责协议通信的组件
3. Server：提供能力的一方
4. Tool：模型可调用的动作
5. Resource：模型可读取的上下文
6. Prompt：可复用的提示词模板
7. Elicitation：Server 请求用户补充信息的交互能力
8. Authorization / Security：访问授权、安全边界和用户确认
"""


def get_docs_resource_template() -> str:
    return """
# MCP Resource Template

Resource Template 是带 URI 参数的动态资源，例如 mcp://concepts/{name}。
"""


def get_docs_stdio() -> str:
    return """
# stdio

stdio 通过标准输入和标准输出传输 MCP 消息。
"""


def get_docs_streamable_http() -> str:
    return """
# streamable-http

streamable-http 是 MCP 的 HTTP 传输方式，默认示例地址可以是 http://127.0.0.1:8000/mcp。
"""


def get_docs_json_rpc() -> str:
    return """
# JSON-RPC

MCP 消息基于 JSON-RPC 结构，常见字段包括 method、params、result 和 error。
"""


def get_docs_lifecycle() -> str:
    return """
# MCP 生命周期

MCP 连接通常从 initialize 开始，然后查询能力并调用工具、读取资源或获取 Prompt。
"""


def get_docs_elicitation() -> str:
    return """
# MCP Elicitation

Elicitation 是 Server 通过 Host 向用户请求补充信息的能力。

它适合用在工具继续执行前必须让用户确认、选择或补齐信息的场景。

学习重点：

1. Server 只提出需要什么信息
2. Host 负责真实用户交互
3. 用户补充信息之后，Server 才能继续后续流程
"""


def get_docs_authorization() -> str:
    return """
# MCP Authorization

Authorization 关注 MCP Server 访问资源和执行动作时的授权边界。

它强调凭证保护、最小权限、用户确认，以及 Host 对敏感操作的控制权。
"""


def get_docs_security() -> str:
    return """
# MCP Security

MCP Security 的核心是把工具、资源、用户数据和外部输入放在清晰的安全边界里。

学习 MCP 时要重点注意：

1. Tool 可能触碰真实文件、网络、数据库或凭证
2. 外部 Resource 内容可能包含 prompt injection
3. 敏感操作应有用户确认
4. Server 不应该默认拥有超出需要的权限
"""


def get_docs_tasks() -> str:
    return """
# MCP Tasks

Tasks 是 MCP 中描述长时间运行任务的实验性方向。

它适合表达需要进度、状态和后续结果的工作流，而不是一次请求立即完成的简单调用。
"""


def get_concept_resource(name: str) -> str:
    """
    这个函数根据名称获取 MCP 概念资源：
    验证输入：去除空格、转小写，确保非空
    查找概念：如果名称不在 CONCEPTS 字典中，返回错误提示和可用概念列表
    返回结果：找到则返回格式化的 Markdown 文档（标题 + 内容）
    用于动态提供 MCP 概念的详细说明。
    :param name:
    :return:
    """
    normalized_name = normalize_key(require_not_blank(name, "name"))

    if normalized_name not in CONCEPTS:
        available_concepts = format_available_items(list(CONCEPTS.keys()))
        return f"没有找到概念：{name}\n\n当前支持的概念包括：\n\n{available_concepts}"

    return f"""
# {normalized_name}

{CONCEPTS[normalized_name].strip()}
"""


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
