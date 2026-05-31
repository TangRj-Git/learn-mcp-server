CONCEPTS = {
    "mcp": """
MCP，全称是 Model Context Protocol，中文可以理解为模型上下文协议。

它的核心作用是让大模型应用能够用一种统一的方式连接外部工具、数据和提示词。

MCP Server 不直接等于大模型，它只是给大模型应用提供可用能力。
""",
    "host": """
Host 是 MCP 架构中的宿主应用。

它通常是用户真正使用的应用，例如 AI 编程工具、聊天应用、IDE、桌面客户端等。
""",
    "client": """
Client 是 Host 内部负责和 MCP Server 通信的组件。

它负责发送初始化请求、获取能力清单、调用工具、读取资源和获取提示词。
""",
    "server": """
Server 是 MCP 架构中提供能力的一方。

MCP Server 可以提供 Tools、Resources 和 Prompts。
""",
    "tool": """
Tool 是 MCP Server 暴露给模型调用的可执行能力。

Tool 适合表示动作、计算、查询、生成、处理等操作。

在 FastMCP 中，可以使用 @mcp.tool() 把一个 Python 函数注册成 MCP Tool。
""",
    "resource": """
Resource 是 MCP Server 暴露出来的可读取上下文资源。

Resource 更像文档、资料、文件、说明书、数据库记录等内容。
""",
    "prompt": """
Prompt 是 MCP Server 提供的可复用提示词模板。

Prompt 适合封装一段固定的任务说明，让用户或模型可以复用。

在 FastMCP 中，可以使用 @mcp.prompt() 注册 Prompt。
""",
    "stdio": """
stdio 是 MCP 的一种本地传输方式。

它通过标准输入和标准输出传输 MCP 消息。

stdio 模式下，不应该随便使用 print 输出普通日志，因为 stdout 是协议通信通道。
""",
    "streamable-http": """
Streamable HTTP 是 MCP 的一种 HTTP 传输方式。

它通常适合远程访问、Web 服务、长期运行的 MCP Server。
""",
    "json-rpc": """
JSON-RPC 是一种基于 JSON 的远程过程调用格式。

MCP 的消息通信基于 JSON-RPC 结构，常见字段包括 jsonrpc、id、method、params、result 和 error。
""",
    "resource-template": """
Resource Template 是带参数的动态 Resource。

它通过 URI 占位符把路径中的值映射到函数参数，例如 mcp://concepts/{name} 会把 name 传给对应函数。

Resource Template 适合按名称、ID、路径或主题动态读取上下文内容。
""",
    "transport": """
Transport 是 MCP Client 和 MCP Server 之间传输 JSON-RPC 消息的通道。

常见 Transport 包括本地 stdio 和基于 HTTP 的 streamable-http。

选择 Transport 时，要先判断 Server 是由 Host 启动，还是作为长期运行的服务被远程访问。
""",
    "sse": """
SSE，全称是 Server-Sent Events，是一种服务端向客户端持续推送事件的 HTTP 技术。

在 MCP 早期或部分生态里，SSE 曾经常被用来承载远程 MCP 通信。

学习 SSE 的重点不是把它和 streamable-http 混为一谈，而是理解它解决的是“服务端持续发送消息”的问题。
""",
    "capability-negotiation": """
能力协商是 MCP Client 和 MCP Server 在连接初始化阶段互相确认支持能力的过程。

Client 会通过 initialize 等消息了解 Server 支持哪些 Tools、Resources、Prompts 或其他能力。

能力协商的意义是让 Host 不需要猜测 Server 能做什么，而是通过协议清单发现可用能力。
""",
    "notification": """
通知是 MCP 中不要求对方返回结果的协议消息。

它适合表达状态变化、进度变化、资源变更等事件。

和普通请求不同，通知通常没有 result，重点是让另一端知道某件事已经发生。
""",
    "sampling": """
采样是 MCP 中让 Server 请求 Host 或模型生成内容的一类能力。

它可以让某些 Server 在需要语言模型能力时，不直接内置模型，而是通过 Host 侧模型完成生成。

学习采样时要注意权限边界：Server 不应该绕过 Host 直接滥用模型能力。
""",
    "roots": """
根目录是 Host 告诉 MCP Server 的可访问工作区范围。

它通常用于让 Server 知道哪些目录、项目或文件范围可以作为上下文来处理。

根目录的意义是限制边界，避免 Server 在不了解上下文范围时访问不该访问的位置。
""",
    "elicitation": """
Elicitation 是 MCP 中 Server 向 Host 请求用户补充信息的一类能力。

它适合在工具调用或工作流继续之前，让用户确认、补充或选择必要信息。

学习 elicitation 时要注意：Server 不能假装用户已经同意，应该由 Host 控制用户交互和授权边界。
""",
    "authorization": """
Authorization 是 MCP 中围绕访问授权、身份和权限边界的设计。

它用于帮助 Host 和 Server 明确谁能访问什么资源、什么时候需要用户同意，以及凭证不能被随意暴露。

学习授权时，不要只看“能不能连上”，还要看最小权限、用户确认和凭证保护。
""",
    "security": """
Security 是 MCP 项目必须持续考虑的安全边界。

它包括工具调用前的用户确认、敏感数据保护、prompt injection 风险、权限最小化和不信任外部输入。

学习 MCP 安全时，要把 Server 看成会接触真实文件、网络或凭证的组件，而不只是一个普通示例函数。
""",
    "tasks": """
Tasks 是 MCP 中用于描述长时间运行任务的实验性方向。

它适合表达需要持续跟踪、可能产生进度或结果更新的工作，而不是一次请求马上返回的简单 Tool 调用。

学习 tasks 时，重点理解它和普通 Tool 的区别：Tool 偏即时调用，长时间运行任务更强调状态、进度和后续结果。
""",
    "config": """
配置是 Host 发现和启动 MCP Server 的入口。

stdio 配置通常依赖 command 和 args，由 Host 启动本地进程。

streamable-http 配置通常依赖 url，由 Host 连接已经运行的 MCP 服务。
""",
    "debug": """
Debug 是 MCP 项目开发中定位启动、注册、配置、传输和调用问题的过程。

常见排查顺序是：先确认环境，再确认启动命令，再确认能力注册，最后确认 Host 是否重新加载配置。
""",
}

LEARNING_MODULES = [
    {
        "name": "MCP 基础概念",
        "topics": ["mcp", "host", "client", "server"],
        "description": "理解 MCP 的整体架构和核心角色。",
    },
    {
        "name": "MCP 原语",
        "topics": ["tool", "resource", "prompt"],
        "description": "学习 Tool、Resource、Prompt 的用途和区别。",
    },
    {
        "name": "MCP 传输方式",
        "topics": ["stdio", "streamable-http"],
        "description": "学习 MCP Server 和 Client 之间如何通信。",
    },
    {
        "name": "MCP 协议消息",
        "topics": ["json-rpc"],
        "description": "理解 MCP 底层消息格式和请求响应结构。",
    },
    {
        "name": "MCP 进阶能力",
        "topics": [
            "sse",
            "capability-negotiation",
            "notification",
            "sampling",
            "roots",
            "elicitation",
            "tasks",
        ],
        "description": "理解 MCP 生态里更深入的通信、能力发现、通知、采样、用户交互和任务状态。",
    },
    {
        "name": "MCP 安全与授权",
        "topics": ["security", "authorization"],
        "description": "学习 MCP 项目里的安全边界、用户确认、权限最小化和凭证保护。",
    },
    {
        "name": "MCP 工程化实践",
        "topics": ["resource-template", "config", "debug"],
        "description": "学习动态资源、Host 配置和常见调试流程。",
    },
]

__all__ = ["CONCEPTS", "LEARNING_MODULES"]
