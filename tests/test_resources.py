import pytest

from learn_mcp_server import server


def call_resource(function_name: str) -> str:
    resource_func = getattr(server, function_name, None)
    assert callable(resource_func), f"{function_name} should be defined"
    return resource_func()


def test_docs_introduction_resource():
    result = call_resource("get_docs_introduction")

    assert "# MCP 简介" in result
    assert "Model Context Protocol" in result


def test_docs_tools_resource():
    result = call_resource("get_docs_tools")

    assert "# MCP Tool" in result
    assert "@mcp.tool()" in result


def test_docs_resources_resource():
    result = call_resource("get_docs_resources")

    assert "# MCP Resource" in result
    assert "@mcp.resource()" in result


def test_docs_prompts_resource():
    result = call_resource("get_docs_prompts")

    assert "# MCP Prompt" in result
    assert "@mcp.prompt()" in result


def test_docs_transports_resource():
    result = call_resource("get_docs_transports")

    assert "# MCP Transport" in result
    assert "stdio" in result
    assert "streamable-http" in result


def test_concept_resource_template_returns_known_concept():
    result = server.get_concept_resource("tool")

    assert "# tool" in result
    assert "可执行能力" in result


def test_concept_resource_template_lists_available_for_unknown_concept():
    result = server.get_concept_resource("unknown")

    assert "没有找到概念" in result
    assert "当前支持的概念包括" in result


def test_concept_resource_template_rejects_empty_name():
    with pytest.raises(ValueError, match="name 不能为空"):
        server.get_concept_resource("   ")


def test_example_resource_template_returns_basic_tool_example():
    result = server.get_example_resource("basic-tool")

    assert "# basic-tool" in result
    assert "@mcp.tool()" in result


def test_example_resource_template_lists_available_for_unknown_example():
    result = server.get_example_resource("unknown")

    assert "没有找到示例" in result
    assert "basic-tool" in result


def test_debug_resource_template_returns_stdio_debug_guide():
    result = server.get_debug_resource("stdio")

    assert "# stdio 调试" in result
    assert "不要使用 print" in result


def test_debug_resource_template_lists_available_for_unknown_error_type():
    result = server.get_debug_resource("unknown")

    assert "没有找到调试文档" in result
    assert "stdio" in result


def test_docs_architecture_resource():
    result = call_resource("get_docs_architecture")

    assert "# MCP 架构" in result
    assert "Host" in result
    assert "Client" in result
    assert "Server" in result


def test_docs_host_client_server_resource():
    result = call_resource("get_docs_host_client_server")

    assert "# Host、Client、Server" in result
    assert "Host" in result
    assert "Client" in result


def test_docs_concepts_resource():
    result = call_resource("get_docs_concepts")

    assert "# MCP 概念总览" in result
    assert "Tool" in result
    assert "Resource" in result
    assert "Prompt" in result


def test_docs_resource_template_resource():
    result = call_resource("get_docs_resource_template")

    assert "# MCP Resource Template" in result
    assert "{name}" in result


def test_docs_stdio_resource():
    result = call_resource("get_docs_stdio")

    assert "# stdio" in result
    assert "标准输入" in result


def test_docs_streamable_http_resource():
    result = call_resource("get_docs_streamable_http")

    assert "# streamable-http" in result
    assert "HTTP" in result


def test_docs_json_rpc_resource():
    result = call_resource("get_docs_json_rpc")

    assert "# JSON-RPC" in result
    assert "method" in result


def test_docs_lifecycle_resource():
    result = call_resource("get_docs_lifecycle")

    assert "# MCP 生命周期" in result
    assert "initialize" in result


def test_static_example_resources():
    assert "# basic-tool" in server.get_example_basic_tool()
    assert "# basic-resource" in server.get_example_basic_resource()
    assert "# resource-template" in server.get_example_resource_template()
    assert "# basic-prompt" in server.get_example_basic_prompt()


def test_legacy_example_resource_aliases():
    assert "# basic-tool" in server.get_example_tool_basic()
    assert "# basic-resource" in server.get_example_resource_basic()
    assert "# basic-prompt" in server.get_example_prompt_basic()


def test_additional_example_resources():
    assert "# tool-params" in server.get_example_tool_params()
    assert "# async-tool" in server.get_example_async_tool()
    assert "# error-handling" in server.get_example_error_handling()
    assert "# end-to-end-client" in server.get_example_end_to_end_client()


def test_advanced_concept_resource_templates():
    assert "Server-Sent Events" in server.get_concept_resource("sse")
    assert "能力协商" in server.get_concept_resource("capability-negotiation")
    assert "通知" in server.get_concept_resource("notification")
    assert "采样" in server.get_concept_resource("sampling")
    assert "根目录" in server.get_concept_resource("roots")


def test_current_spec_concept_resource_templates():
    assert "用户补充信息" in server.get_concept_resource("elicitation")
    assert "授权" in server.get_concept_resource("authorization")
    assert "安全边界" in server.get_concept_resource("security")
    assert "长时间运行" in server.get_concept_resource("tasks")


def test_current_spec_docs_resources():
    assert "# MCP Elicitation" in server.get_docs_elicitation()
    assert "用户补充信息" in server.get_docs_elicitation()
    assert "# MCP Authorization" in server.get_docs_authorization()
    assert "授权" in server.get_docs_authorization()
    assert "# MCP Security" in server.get_docs_security()
    assert "安全边界" in server.get_docs_security()
    assert "# MCP Tasks" in server.get_docs_tasks()
    assert "长时间运行" in server.get_docs_tasks()


def test_debug_common_errors_resource():
    result = call_resource("get_debug_common_errors")

    assert "# 常见错误" in result
    assert "用户机器没有安装 uv" in result
    assert "uvx" in result


def test_config_resource_template_returns_stdio_config():
    result = server.get_config_resource("stdio")

    assert "# stdio 配置" in result
    assert "mcpServers" in result


def test_config_resource_template_returns_http_config():
    result = server.get_config_resource("streamable-http")

    assert "# streamable-http 配置" in result
    assert "http://127.0.0.1:8000/mcp" in result


def test_config_resource_template_lists_available_for_unknown_config():
    result = server.get_config_resource("unknown")

    assert "没有找到配置文档" in result
    assert "stdio" in result


def test_static_config_resources():
    assert "# stdio 配置" in server.get_docs_config_stdio()
    assert '"command": "uvx"' in server.get_docs_config_stdio()
    assert '"command": "uv"' in server.get_docs_config_stdio()
    assert "python.exe" not in server.get_docs_config_stdio()
    assert "# streamable-http 配置" in server.get_docs_config_http()
    assert "# 本地配置和远程配置" in server.get_docs_config_local_vs_remote()
    assert "# 配置常见错误" in server.get_docs_config_common_errors()


def test_additional_debug_resources():
    assert "# stdio 错误" in server.get_debug_stdio_errors()
    assert "# HTTP 错误" in server.get_debug_http_errors()
    assert "# 配置错误" in server.get_debug_config_errors()


def test_static_curriculum_resources():
    beginner = server.get_curriculum_beginner()
    intermediate = server.get_curriculum_intermediate()
    advanced = server.get_curriculum_advanced()

    assert "# MCP Beginner 课程" in beginner
    assert "第 1 课" in beginner
    assert "Tool" in beginner
    assert "# MCP Intermediate 课程" in intermediate
    assert "Resource Template" in intermediate
    assert "# MCP Advanced 课程" in advanced
    assert "sampling" in advanced


def test_curriculum_resource_template_returns_known_level():
    result = server.get_curriculum_resource("beginner")

    assert "# MCP Beginner 课程" in result
    assert "学习目标" in result


def test_curriculum_resource_template_lists_available_for_unknown_level():
    result = server.get_curriculum_resource("unknown")

    assert "没有找到课程" in result
    assert "beginner" in result
    assert "advanced" in result


def test_curriculum_resource_template_rejects_empty_level():
    with pytest.raises(ValueError, match="level 不能为空"):
        server.get_curriculum_resource("   ")
