"""官方出处与版本标签；日期表示实际核对日，不随启动自动更新。"""

from learn_mcp_server.settings import PROTOCOL_REVISION

CHECKED_AT = "2026-10-09"
BASELINE = f"FastMCP 4.x / MCP Python SDK 2.x / 协议 {PROTOCOL_REVISION}"
MCP_NEW = "https://modelcontextprotocol.io/specification/2026-07-28"
FASTMCP = "https://gofastmcp.com"

TOPIC_SOURCES = {
    "mcp": f"{MCP_NEW}/index",
    "host": "https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture",
    "client": f"{FASTMCP}/clients/client",
    "server": f"{FASTMCP}/servers/server",
    "tool": f"{MCP_NEW}/server/tools",
    "resource": f"{MCP_NEW}/server/resources",
    "prompt": f"{MCP_NEW}/server/prompts",
    "resource-template": f"{FASTMCP}/servers/resources",
    "transport": f"{MCP_NEW}/basic/transports/index",
    "stdio": f"{MCP_NEW}/basic/transports/stdio",
    "streamable-http": f"{MCP_NEW}/basic/transports/streamable-http",
    "sse": f"{MCP_NEW}/basic/transports/streamable-http",
    "json-rpc": f"{MCP_NEW}/basic/index",
    "lifecycle": f"{MCP_NEW}/basic/versioning",
    "capability-negotiation": f"{MCP_NEW}/basic/versioning",
    "notification": f"{MCP_NEW}/basic/index",
    "schema": f"{FASTMCP}/servers/tools",
    "structured-output": f"{FASTMCP}/clients/tools",
    "errors": f"{MCP_NEW}/server/tools",
    "context": f"{FASTMCP}/servers/context",
    "progress": f"{FASTMCP}/servers/progress",
    "cancellation": f"{MCP_NEW}/basic/patterns/cancellation",
    "logging": f"{MCP_NEW}/server/utilities/logging",
    "sampling": f"{MCP_NEW}/client/sampling",
    "roots": f"{MCP_NEW}/client/roots",
    "elicitation": f"{MCP_NEW}/client/elicitation",
    "authorization": f"{MCP_NEW}/basic/authorization/index",
    "security": "https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security",
    "tasks": "https://modelcontextprotocol.io/extensions/tasks/overview",
    "config": f"{FASTMCP}/integrations/mcp-json-configuration",
    "debug": "https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector",
    "tests": f"{FASTMCP}/servers/testing",
    "completion": f"{MCP_NEW}/server/utilities/completion",
    "pagination": f"{MCP_NEW}/server/utilities/pagination",
    "latest-protocol": f"{MCP_NEW}/changelog",
    "discovery": f"{MCP_NEW}/server/discover",
    "mrtr": f"{MCP_NEW}/basic/patterns/mrtr",
    "subscriptions": f"{MCP_NEW}/basic/patterns/subscriptions",
    "caching": f"{MCP_NEW}/server/utilities/caching",
    "extensions": "https://modelcontextprotocol.io/extensions/overview",
    "apps": "https://modelcontextprotocol.io/extensions/apps/overview",
    "skills": "https://modelcontextprotocol.io/extensions/skills/overview",
}

LATEST_TOPICS = {
    "latest-protocol",
    "discovery",
    "mrtr",
    "subscriptions",
    "caching",
    "extensions",
    "apps",
    "skills",
}
DEPRECATED_TOPICS = {"roots", "sampling", "logging"}


def reference_note(topic: str) -> str:
    """为正文附上可追溯版本说明，不声称已实现全部能力。"""
    if topic in {"latest-protocol", "discovery"}:
        version = f"当前规范：{BASELINE}；现代发现/调用已验证，可选交互须独立验收。"
    elif topic in LATEST_TOPICS:
        version = f"当前规范：{BASELINE}；可选专题只讲解，具体能力以服务发现和测试为准。"
    elif topic in DEPRECATED_TOPICS:
        version = "旧版历史能力；2026-07-28 已弃用但暂未删除。"
    else:
        version = f"主课程：{BASELINE}；旧握手与已弃用能力另有历史标记。"
    url = TOPIC_SOURCES[topic]
    return f"\n\n适用版本：{version}\n\n官方出处：[查看文档]({url})\n\n内容核对日期：{CHECKED_AT}"


__all__ = [
    "BASELINE",
    "CHECKED_AT",
    "DEPRECATED_TOPICS",
    "LATEST_TOPICS",
    "TOPIC_SOURCES",
    "reference_note",
]
