import json

import pytest

from learn_mcp_server.tools.basic_tools import (
    get_learning_path,
    get_server_info,
    list_learning_modules,
)
from learn_mcp_server.tools.concept_tools import compare_concepts, explain_concept, get_concept_map
from learn_mcp_server.tools.config_tools import (
    compare_local_and_remote_config,
    explain_config,
    generate_http_config,
    generate_stdio_config,
)
from learn_mcp_server.tools.debug_tools import (
    diagnose_issue,
    explain_error_message,
    list_common_errors,
)
from learn_mcp_server.tools.example_tools import (
    explain_code_example,
    get_code_example,
    list_code_examples,
)
from learn_mcp_server.tools.practice_tools import (
    check_answer,
    generate_learning_plan,
    get_practice_task,
    suggest_next_step,
)


def test_get_server_info_contains_project_name():
    result = get_server_info()

    assert "learn-mcp-server" in result
    assert "get_server_info" in result


def test_list_learning_modules_contains_basic_modules():
    result = list_learning_modules()

    assert "MCP 基础概念" in result
    assert "MCP 原语" in result
    assert "MCP 传输方式" in result
    assert "MCP 进阶能力" in result
    assert "sampling" in result


def test_get_learning_path_contains_ordered_study_steps():
    result = get_learning_path()

    assert "# MCP 学习路径" in result
    assert "第 1 步" in result
    assert "Tool" in result
    assert "Resource" in result
    assert "Prompt" in result


def test_explain_concept_returns_known_concept():
    result = explain_concept("tool")

    assert "# tool" in result
    assert "Tool 是 MCP Server 暴露给模型调用的可执行能力" in result


def test_explain_concept_returns_advanced_concepts():
    assert "Server-Sent Events" in explain_concept("sse")
    assert "能力协商" in explain_concept("capability-negotiation")
    assert "通知" in explain_concept("notification")
    assert "采样" in explain_concept("sampling")
    assert "根目录" in explain_concept("roots")
    assert "Resource Template" in explain_concept("resource-template")


def test_explain_concept_returns_current_spec_concepts():
    assert "用户补充信息" in explain_concept("elicitation")
    assert "授权" in explain_concept("authorization")
    assert "安全边界" in explain_concept("security")
    assert "长时间运行" in explain_concept("tasks")


def test_explain_concept_rejects_empty_input():
    with pytest.raises(ValueError, match="concept 不能为空"):
        explain_concept("   ")


def test_explain_concept_lists_available_concepts_for_unknown_input():
    result = explain_concept("unknown")

    assert "没有找到概念" in result
    assert "当前支持的概念包括" in result
    assert "mcp" in result


def test_compare_concepts_returns_both_concepts():
    result = compare_concepts("tool", "resource")

    assert "# tool 和 resource 的对比" in result
    assert "## tool" in result
    assert "## resource" in result


def test_get_concept_map_contains_core_relationships():
    result = get_concept_map()

    assert "# MCP 概念地图" in result
    assert "Host" in result
    assert "Client" in result
    assert "Server" in result
    assert "Tool" in result
    assert "Resource" in result
    assert "Prompt" in result


def test_compare_concepts_rejects_empty_left():
    with pytest.raises(ValueError, match="left 不能为空"):
        compare_concepts("   ", "tool")


def test_compare_concepts_rejects_empty_right():
    with pytest.raises(ValueError, match="right 不能为空"):
        compare_concepts("tool", "   ")


def test_get_code_example_returns_basic_tool_example():
    result = get_code_example("basic-tool")

    assert "# basic-tool" in result
    assert "@mcp.tool()" in result


def test_get_code_example_lists_available_for_unknown_topic():
    result = get_code_example("unknown")

    assert "没有找到示例" in result
    assert "basic-tool" in result


def test_list_code_examples_contains_available_examples():
    result = list_code_examples()

    assert "# MCP 示例清单" in result
    assert "basic-tool" in result
    assert "async-tool" in result
    assert "error-handling" in result
    assert "end-to-end-client" in result


def test_get_code_example_returns_end_to_end_client_example():
    result = get_code_example("end-to-end-client")

    assert "# end-to-end-client" in result
    assert "Client" in result
    assert "list_tools" in result
    assert "call_tool" in result


def test_explain_code_example_returns_explanation():
    result = explain_code_example("basic-tool")

    assert "basic-tool" in result
    assert "注册成模型可调用的 Tool" in result


def test_generate_learning_plan_for_beginner():
    result = generate_learning_plan("beginner")

    assert "MCP 入门学习计划" in result
    assert "第 1 天" in result


def test_get_practice_task_returns_topic_task():
    result = get_practice_task("tool")

    assert "Tool 练习" in result
    assert "get_server_info" in result


def test_get_practice_task_returns_advanced_topic_tasks():
    assert "Resource Template 练习" in get_practice_task("resource-template")
    assert "Transport 练习" in get_practice_task("transport")
    assert "JSON-RPC 练习" in get_practice_task("json-rpc")
    assert "Elicitation 练习" in get_practice_task("elicitation")
    assert "Security 练习" in get_practice_task("security")
    assert "Debug 练习" in get_practice_task("debug")


def test_check_answer_gives_feedback_for_relevant_answer():
    result = check_answer("tool", "Tool 使用 @mcp.tool 注册，适合执行动作。")

    assert "不是语义判卷" in result
    assert "请核对实际含义" in result
    assert "Tool" in result


def test_explain_config_detects_stdio_config():
    result = explain_config(
        '{"mcpServers": {"learn": {"command": "python", "args": ["server.py"]}}}'
    )

    assert "stdio" in result
    assert "command" in result


def test_explain_config_rejects_invalid_json():
    result = explain_config("{bad json")

    assert "不是合法的 JSON" in result


def test_generate_stdio_config_returns_valid_mcp_json():
    result = generate_stdio_config("python", ["server.py"])
    config = json.loads(result)

    server = config["mcpServers"]["learn-mcp-server"]
    assert server["command"] == "python"
    assert server["args"] == ["server.py"]


def test_generate_stdio_config_rejects_empty_command():
    with pytest.raises(ValueError, match="command 不能为空"):
        generate_stdio_config("   ", ["server.py"])


def test_generate_stdio_config_rejects_non_list_args():
    with pytest.raises(ValueError, match="args 必须是字符串列表"):
        generate_stdio_config("python", "server.py")


def test_generate_stdio_config_rejects_non_string_args():
    with pytest.raises(ValueError, match="args 必须是字符串列表"):
        generate_stdio_config("python", ["server.py", 123])


def test_generate_http_config_returns_valid_mcp_json():
    result = generate_http_config("http://127.0.0.1:8000/mcp")
    config = json.loads(result)

    server = config["mcpServers"]["learn-mcp-server-http"]
    assert server["url"] == "http://127.0.0.1:8000/mcp"


def test_generate_http_config_rejects_empty_url():
    with pytest.raises(ValueError, match="server_url 不能为空"):
        generate_http_config("   ")


def test_compare_local_and_remote_config_mentions_transport_differences():
    result = compare_local_and_remote_config()

    assert "# 本地配置和远程配置对比" in result
    assert "stdio" in result
    assert "streamable-http" in result
    assert "command" in result
    assert "url" in result


def test_diagnose_issue_for_stdio_output_problem():
    result = diagnose_issue("stdio 模式下我用了 print，Host 看不到工具")

    assert "stdio" in result
    assert "print" in result


def test_diagnose_issue_for_dependency_problem_mentions_uv():
    result = diagnose_issue("ModuleNotFoundError: No module named fastmcp")

    assert "uv" in result
    assert "uvx" in result
    assert "conda" not in result
    assert "python.exe" not in result


def test_suggest_next_step_returns_follow_up_topic():
    result = suggest_next_step("tool")

    assert "# 下一步学习建议" in result
    assert "Resource" in result
    assert "Prompt" in result


def test_explain_error_message_classifies_common_error():
    result = explain_error_message("ModuleNotFoundError: No module named 'fastmcp'")

    assert "# 错误消息解释" in result
    assert "uv" in result
    assert "fastmcp" in result


def test_list_common_errors_contains_known_errors():
    result = list_common_errors()

    assert "启动命令" in result
    assert "uvx" in result
    assert "Resource URI 写错" in result
