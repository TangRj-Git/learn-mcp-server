"""从 MCP Client 观察完整教学示例，覆盖输入、输出与失败。"""

import ast
import asyncio
import json
import re

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError
from mcp.shared.exceptions import MCPError

from learn_mcp_server.data.examples import CODE_EXAMPLES
from learn_mcp_server.demo import mcp


def test_demo_schema_results_error_modes_and_context_injection():
    async def check():
        async with Client(mcp) as client:
            tools = {tool.name: tool for tool in await client.list_tools()}
            schema = tools["divide"].input_schema
            assert set(schema["required"]) == {"a", "b"}
            assert schema["properties"]["mode"]["enum"] == ["exact", "rounded"]
            assert schema["properties"]["b"]["description"]
            assert tools["divide"].output_schema["type"] == "object"
            assert "ctx" not in tools["count_steps"].input_schema["properties"]
            result = await client.call_tool("divide", {"a": 1, "b": 3, "mode": "rounded"})
            assert result.structured_content == {"value": 0.33}
            assert result.content and result.data == {"value": 0.33}
            error = await client.call_tool("divide", {"a": 1, "b": 0}, raise_on_error=False)
            assert error.is_error and "不能为零" in error.content[0].text
            with pytest.raises(ToolError):
                await client.call_tool("divide", {"a": 1, "b": 0})
            error = await client.call_tool(
                "divide", {"a": 1, "b": 2, "mode": "bad"}, raise_on_error=False
            )
            assert error.is_error
            # 当前 FastMCP v4 将未知工具也转换成工具错误结果，不凭规范猜测 SDK 行为。
            unknown = await client.call_tool_mcp("unknown_tool", {})
            assert unknown.is_error and "unknown_tool" in unknown.content[0].text

    asyncio.run(check())


def test_demo_resources_query_parameters_and_prompt_wire_conversion():
    async def check():
        async with Client(mcp) as client:
            metadata = (await client.read_resource("demo://metadata"))[0]
            assert metadata.mime_type == "application/json"
            assert json.loads(metadata.text)["protocol"] == "2026-07-28"
            simple = (await client.read_resource("demo://topics/tool"))[0]
            detailed = (await client.read_resource("demo://topics/tool?detail=true"))[0]
            other = (await client.read_resource("demo://topics/resource"))[0]
            assert simple.mime_type == detailed.mime_type == "text/markdown"
            assert simple.text != detailed.text and simple.text != other.text
            encoded = (await client.read_resource("demo://topics/%74ool"))[0]
            assert encoded.text == simple.text
            with pytest.raises(MCPError, match="未知主题"):
                await client.read_resource("demo://topics/unknown")
            with pytest.raises(MCPError, match="未知主题"):
                await client.read_resource("demo://topics/tool%2Fresource")
            with pytest.raises(MCPError, match="boolean"):
                await client.read_resource("demo://topics/tool?detail=bad")
            prompt = await client.get_prompt("explain_topic", {"topic": "tool"})
            assert [message.role for message in prompt.messages] == ["user", "assistant"]
            plan = await client.get_prompt("study_plan", {"days": "3", "level": "advanced"})
            assert "3 天" in plan.messages[0].content.text
            with pytest.raises(MCPError):
                await client.get_prompt("study_plan", {"days": "0"})

    asyncio.run(check())


def test_demo_progress_callback_is_observable():
    events = []

    async def handler(progress, total, message):
        events.append((progress, total))

    async def check():
        async with Client(mcp) as client:
            result = await client.call_tool("count_steps", {}, progress_handler=handler)
            assert result.structured_content == {"steps": 3}

    asyncio.run(check())
    assert events == [(1, 3), (2, 3), (3, 3)]


def test_packaged_learning_examples_are_valid_and_complete_source_is_runnable():
    for name, text in CODE_EXAMPLES.items():
        for block in re.findall(r"```python\n(.*?)```", text, re.S):
            ast.parse(block, filename=f"example:{name}")
    source = re.findall(r"```python\n(.*?)```", CODE_EXAMPLES["minimal-server"], re.S)[0]
    scope = {"__name__": "learning_example_test"}
    exec(compile(source, "minimal-server", "exec"), scope)

    async def check():
        async with Client(scope["mcp"]) as client:
            result = await client.call_tool("divide", {"a": 8, "b": 2})
            assert result.structured_content == {"value": 4}

    asyncio.run(check())
