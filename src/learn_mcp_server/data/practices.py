PRACTICE_TASKS = {
    "tool": {
        "title": "Tool 练习",
        "task": "实现一个 get_server_info Tool，返回 Server 名称、用途和当前支持的能力。",
        "keywords": ["tool", "@mcp.tool", "动作", "执行"],
    },
    "resource": {
        "title": "Resource 练习",
        "task": "实现一个 mcp://docs/introduction Resource，返回一段 MCP 入门文档。",
        "keywords": ["resource", "@mcp.resource", "uri", "上下文"],
    },
    "prompt": {
        "title": "Prompt 练习",
        "task": "实现一个 explain_mcp_topic Prompt，根据主题和水平生成讲解提示词。",
        "keywords": ["prompt", "@mcp.prompt", "模板", "提示词"],
    },
    "resource-template": {
        "title": "Resource Template 练习",
        "task": "实现一个 mcp://concepts/{name} Resource Template，根据 name 返回不同概念文档。",
        "keywords": ["resource template", "@mcp.resource", "{name}", "动态资源", "uri"],
    },
    "transport": {
        "title": "Transport 练习",
        "task": "对比 stdio 和 streamable-http，说明它们分别适合什么运行场景。",
        "keywords": ["transport", "stdio", "streamable-http", "通信"],
    },
    "json-rpc": {
        "title": "JSON-RPC 练习",
        "task": "写出一个 MCP 请求消息包含哪些关键字段，并解释 method、params、result、error 的作用。",
        "keywords": ["json-rpc", "method", "params", "result", "error"],
    },
    "config": {
        "title": "Config 练习",
        "task": "分别生成一个 stdio 配置和一个 streamable-http 配置，并解释 command、args、url 的区别。",
        "keywords": ["config", "mcpServers", "command", "args", "url"],
    },
    "elicitation": {
        "title": "Elicitation 练习",
        "task": "设计一个需要用户补充信息才能继续的 MCP 场景，说明 Server 应该请求什么、Host 应该如何让用户确认。",
        "keywords": ["elicitation", "用户", "补充信息", "确认", "Host"],
    },
    "security": {
        "title": "Security 练习",
        "task": "列出一个 MCP Tool 访问本地文件或网络前需要做的安全检查，包括用户确认、最小权限和输入校验。",
        "keywords": ["security", "授权", "用户确认", "最小权限", "输入校验"],
    },
    "debug": {
        "title": "Debug 练习",
        "task": "假设 Host 看不到工具，按环境、启动命令、注册表、Host 重载的顺序写出排查步骤。",
        "keywords": ["debug", "环境", "启动", "注册", "Host"],
    },
}

__all__ = ["PRACTICE_TASKS"]
