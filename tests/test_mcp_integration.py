import asyncio

from fastmcp import Client

from learn_mcp_server.server import mcp


def run_async(coro):
    return asyncio.run(coro)


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
        assert {template.uriTemplate for template in resource_templates} >= {
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
