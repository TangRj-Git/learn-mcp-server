"""在仓库外、独立环境验证 wheel 内容；由本地验收和 CI 共用。"""

import asyncio
import json
import sys
from importlib.metadata import version
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

import learn_mcp_server
from learn_mcp_server.demo import mcp as demo
from learn_mcp_server.server import create_server
from learn_mcp_server.settings import PROTOCOL_REVISION


async def main() -> None:
    package_file = Path(learn_mcp_server.__file__).resolve()
    workspace = Path(__file__).resolve().parents[1]
    assert workspace not in package_file.parents, "必须从独立环境的 wheel 导入项目。"
    assert Path.cwd() != workspace, "请在仓库外运行本脚本。"
    async with Client(create_server(), timeout=10) as client:
        assert client.protocol_version == PROTOCOL_REVISION
        assert client.server_info.version == learn_mcp_server.__version__
        tools = await client.list_tools()
        resources = await client.list_resources()
        templates = await client.list_resource_templates()
        prompts = await client.list_prompts()
        assert (len(tools), len(resources), len(templates), len(prompts)) == (20, 39, 5, 5)
        example = await client.call_tool("get_code_example", {"topic": "minimal-server"})
        assert "def divide(" in example.data and "if __name__" in example.data
        document = (await client.read_resource("mcp://examples/minimal-server"))[0]
        assert document.mime_type == "text/markdown" and "def divide(" in document.text
        concept = (await client.read_resource("mcp://concepts/tool"))[0]
        assert "model-controlled" in concept.text
    async with Client(demo, timeout=10) as client:
        result = await client.call_tool("divide", {"a": 8, "b": 2})
        assert result.structured_content == {"value": 4.0}
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "learn_mcp_server.server"],
        cwd=str(Path.cwd()),
        env={"LEARN_MCP_TRANSPORT": "stdio", "PYTHONIOENCODING": "utf-8"},
        keep_alive=False,
    )
    async with Client(transport, timeout=10, init_timeout=10) as client:
        assert client.protocol_version == PROTOCOL_REVISION
        result_from_process = await client.call_tool("explain_concept", {"concept": "tool"})
        assert "model-controlled" in result_from_process.data
    print(
        json.dumps(
            {
                "package_file": str(package_file),
                "fastmcp": version("fastmcp"),
                "mcp": version("mcp"),
                "protocol_version": PROTOCOL_REVISION,
                "capabilities": [20, 39, 5, 5],
                "packaged_example_and_resource": "passed",
                "demo_result": result.structured_content,
                "installed_stdio": "passed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
