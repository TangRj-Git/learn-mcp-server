from learn_mcp_server import server


def test_explain_mcp_topic_prompt():
    result = server.explain_mcp_topic("tool", "beginner")

    assert "请用 beginner 水平" in result
    assert "tool" in result
    assert "示例" in result


def test_generate_mcp_study_plan_prompt():
    result = server.generate_mcp_study_plan("beginner", 3)

    assert "3 天" in result
    assert "MCP" in result
    assert "每天" in result


def test_review_mcp_code_prompt():
    result = server.review_mcp_code("@mcp.tool()\ndef hello() -> str:\n    return 'hi'")

    assert "审查下面这段 MCP 代码" in result
    assert "@mcp.tool()" in result


def test_debug_mcp_error_prompt():
    result = server.debug_mcp_error("ModuleNotFoundError: No module named fastmcp")

    assert "诊断下面这个 MCP 错误" in result
    assert "ModuleNotFoundError" in result


def test_summarize_mcp_concept_prompt():
    result = server.summarize_mcp_concept("resource")

    assert "总结 MCP 概念" in result
    assert "resource" in result
