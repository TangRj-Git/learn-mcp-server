import asyncio

import pytest
from fastmcp import Client

from learn_mcp_server import __version__
from learn_mcp_server.data.concepts import CONCEPTS
from learn_mcp_server.data.configs import CONFIG_DOCS, DEBUG_GUIDES
from learn_mcp_server.data.curriculum import CURRICULUMS
from learn_mcp_server.data.examples import CODE_EXAMPLES
from learn_mcp_server.server import mcp
from learn_mcp_server.settings import PROTOCOL_REVISION


def run_async(coro):
    return asyncio.run(coro)


@pytest.mark.parametrize(
    ("mode", "revision"),
    [("auto", PROTOCOL_REVISION), (PROTOCOL_REVISION, PROTOCOL_REVISION), ("legacy", "2025-11-25")],
)
def test_protocol_modes_identity_and_wire_aliases(mode, revision):
    async def check():
        async with Client(mcp, mode=mode) as client:
            assert client.protocol_version == revision
            if mode in {"auto", "legacy"}:
                assert client.server_info.version == __version__
            tool = (await client.list_tools())[0]
            assert tool.input_schema["type"] == "object"
            assert "inputSchema" in tool.model_dump(by_alias=True)

    run_async(check())


def test_mcp_client_lists_registered_capabilities():
    async def check_capabilities():
        async with Client(mcp) as client:
            tools = await client.list_tools()
            resources = await client.list_resources()
            resource_templates = await client.list_resource_templates()
            prompts = await client.list_prompts()

        assert {tool.name for tool in tools} >= {
            "get_server_info",
            "get_learning_path",
            "explain_concept",
            "get_concept_map",
            "list_code_examples",
            "explain_config",
            "generate_stdio_config",
            "generate_http_config",
            "compare_local_and_remote_config",
            "diagnose_issue",
            "suggest_next_step",
            "explain_error_message",
        }
        assert {str(resource.uri) for resource in resources} >= {
            "mcp://docs/introduction",
            "mcp://docs/authorization",
            "mcp://docs/elicitation",
            "mcp://docs/security",
            "mcp://docs/tasks",
            "mcp://examples/basic-tool",
            "mcp://debug/common-errors",
            "mcp://curriculum/beginner",
            "mcp://curriculum/intermediate",
            "mcp://curriculum/advanced",
        }
        assert {template.uri_template for template in resource_templates} >= {
            "mcp://concepts/{name}",
            "mcp://examples/{name}",
            "mcp://configs/{name}",
            "mcp://debug/{error_type}",
            "mcp://curriculum/{level}",
        }
        assert {prompt.name for prompt in prompts} >= {
            "explain_mcp_topic",
            "generate_mcp_study_plan",
            "review_mcp_code",
            "debug_mcp_error",
            "summarize_mcp_concept",
        }

    run_async(check_capabilities())


def test_mcp_client_can_call_tool_read_resource_and_get_prompt():
    async def check_usage():
        async with Client(mcp) as client:
            tool_result = await client.call_tool("explain_concept", {"concept": "tool"})
            resource_result = await client.read_resource("mcp://docs/introduction")
            prompt_result = await client.get_prompt(
                "explain_mcp_topic",
                {"topic": "resource", "level": "beginner"},
            )

        assert "Tool 是 MCP Server" in tool_result.data
        assert "Model Context Protocol" in resource_result[0].text
        assert "resource" in prompt_result.messages[0].content.text

    run_async(check_usage())


def test_all_registered_documents_and_templates_are_readable_markdown():
    async def check():
        async with Client(mcp) as client:
            resources = await client.list_resources()
            for item in resources:
                assert item.description and item.mime_type == "text/markdown"
                contents = await client.read_resource(str(item.uri))
                assert contents[0].mime_type == "text/markdown" and contents[0].text.strip()
            for category, data in (
                ("concepts", CONCEPTS),
                ("examples", CODE_EXAMPLES),
                ("curriculum", CURRICULUMS),
                ("configs", CONFIG_DOCS),
                ("debug", DEBUG_GUIDES),
            ):
                for key in data:
                    content = (await client.read_resource(f"mcp://{category}/{key.upper()}"))[0]
                    assert content.mime_type == "text/markdown" and content.text.strip()
            for item in await client.list_prompts():
                assert item.description
            for tool in await client.list_tools():
                assert tool.annotations.read_only_hint is True
                assert tool.annotations.open_world_hint is False

    run_async(check())
