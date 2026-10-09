"""内存 Client 的完整闭环；不验证子进程或网络。"""

import argparse
import asyncio
import json

from fastmcp import Client


async def check_connection(client: Client, *, demo: bool = False) -> dict:
    """共同检查发现、Tool、静态/模板 Resource、Prompt。"""
    tools = await client.list_tools()
    resources = await client.list_resources()
    templates = await client.list_resource_templates()
    prompts = await client.list_prompts()
    if demo:
        result = await client.call_tool("divide", {"a": 6, "b": 2})
        resource = await client.read_resource("demo://metadata")
        template = await client.read_resource("demo://topics/tool?detail=true")
        prompt = await client.get_prompt("explain_topic", {"topic": "tool"})
        error = await client.call_tool("divide", {"a": 1, "b": 0}, raise_on_error=False)
        progress = []

        async def handler(value, total, message):
            progress.append({"progress": value, "total": total, "message": message})

        steps = await client.call_tool("count_steps", {}, progress_handler=handler)
        assert error.is_error
        assert result.structured_content == {"value": 3.0}
        assert steps.structured_content == {"steps": 3}
        assert [event["progress"] for event in progress] == [1, 2, 3]
    else:
        result = await client.call_tool("get_server_info", {})
        resource = await client.read_resource("mcp://docs/introduction")
        # 大写路径避开同名静态 URI，确保这次实际走 Template。
        template = await client.read_resource("mcp://concepts/TOOL")
        prompt = await client.get_prompt(
            "explain_mcp_topic", {"topic": "tool", "level": "beginner"}
        )
        progress = []
    assert resource and template and prompt.messages
    assert template[0].mime_type == "text/markdown"
    return {
        "protocol_version": client.protocol_version,
        "server_version": client.server_info.version if client.server_info else None,
        "tools": [tool.name for tool in tools],
        "resources": len(resources),
        "resource_templates": [template.uri_template for template in templates],
        "prompts": [item.name for item in prompts],
        "tool_data": result.data,
        "resource_mime": resource[0].mime_type,
        "template_mime": template[0].mime_type,
        "prompt_roles": [message.role for message in prompt.messages],
        "progress": progress,
    }


async def main(demo: bool = False, mode: str = "auto") -> None:
    if demo:
        from learn_mcp_server.demo import mcp
    else:
        from learn_mcp_server.server import mcp
    async with Client(mcp, timeout=10, mode=mode) as client:
        result = await check_connection(client, demo=demo)
    print(json.dumps({"transport": "in-memory", **result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="检查完整教学示例，包含错误与进度")
    parser.add_argument("--mode", choices=["auto", "2026-07-28", "legacy"], default="auto")
    args = parser.parse_args()
    asyncio.run(main(args.demo, args.mode))
