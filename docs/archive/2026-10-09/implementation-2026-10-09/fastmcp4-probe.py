"""仅在 FastMCP 4 隔离环境运行的研究探针，不属于主服务入口。"""

import asyncio
import json
import sys
from importlib.metadata import version

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from learn_mcp_server.demo import mcp as demo
from learn_mcp_server.server import create_server


async def observe(client):
    async with client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        templates = await client.list_resource_templates()
        prompts = await client.list_prompts()
        result = await client.call_tool("get_server_info", {})
        return {
            "protocol_version": client.protocol_version,
            "server_name": client.server_info.name,
            "server_version": client.server_info.version,
            "capabilities": [len(tools), len(resources), len(templates), len(prompts)],
            "tool_result_nonempty": bool(result.data),
        }


async def main():
    memory = await observe(Client(create_server(), timeout=10))
    stdio = await observe(
        Client(
            StdioTransport(
                command=sys.executable,
                args=["-m", "learn_mcp_server.server"],
                env={"LEARN_MCP_TRANSPORT": "stdio", "PYTHONIOENCODING": "utf-8"},
                keep_alive=False,
            ),
            timeout=10,
        )
    )
    async with Client(demo, timeout=10) as client:
        result = await client.call_tool("divide", {"a": 8, "b": 2})
        unknown = await client.call_tool_mcp("unknown_tool", {})
        assert result.structured_content == {"value": 4.0}
        assert unknown.is_error
    print(
        json.dumps(
            {
                "fastmcp": version("fastmcp"),
                "mcp": version("mcp"),
                "in_memory": memory,
                "stdio": stdio,
                "demo_result": result.structured_content,
                "unknown_tool_is_error": unknown.is_error,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
