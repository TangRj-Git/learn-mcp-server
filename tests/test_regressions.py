"""审计中已复现的问题与对应业务边界。"""

import json

import pytest

from learn_mcp_server.data.concepts import CONCEPTS, LEARNING_MODULES
from learn_mcp_server.data.curriculum import LEARNING_SEQUENCE
from learn_mcp_server.data.references import TOPIC_SOURCES
from learn_mcp_server.prompts.learning_prompts import generate_mcp_study_plan, review_mcp_code
from learn_mcp_server.settings import get_http_port
from learn_mcp_server.tools.config_tools import explain_config, generate_http_config
from learn_mcp_server.tools.debug_tools import diagnose_issue, explain_error_message
from learn_mcp_server.tools.practice_tools import (
    check_answer,
    generate_learning_plan,
    suggest_next_step,
)


@pytest.mark.parametrize("value", [[], None, "value", 42, True])
def test_config_rejects_nonobject_json_without_crashing(value):
    assert "配置根必须是 JSON 对象" in explain_config(json.dumps(value))


@pytest.mark.parametrize(
    "config",
    [
        {"command": 1},
        {"command": " "},
        {"command": "python", "args": "server.py"},
        {"command": "python", "args": [1]},
        {"command": "python", "env": {"TOKEN": 1}},
        {"url": "javascript:alert(1)"},
        {"url": "https://example.com/mcp", "args": []},
    ],
)
def test_invalid_fields_are_reported_per_server(config):
    result = explain_config(json.dumps({"mcpServers": {"learn": config}}))
    assert "配置错误" in result
    assert "这是一个 stdio 配置" not in result
    assert "这是一个 streamable-http 配置" not in result


def test_config_transport_conflict_and_secret_redaction():
    conflict = {"command": "python", "url": "https://example.com/mcp"}
    assert "配置冲突" in explain_config(json.dumps({"mcpServers": {"learn": conflict}}))
    config = {
        "command": "python",
        "args": ["--token", "argument-secret"],
        "env": {"TOKEN": "environment-secret"},
    }
    result = explain_config(json.dumps({"mcpServers": {"learn": config}}))
    assert "argument-secret" not in result and "environment-secret" not in result
    assert "TOKEN" in result and "stdio" in result
    result = explain_config(
        json.dumps({"mcpServers": {"learn": {"url": "https://example.com/mcp?token=query-secret"}}})
    )
    assert "query-secret" not in result and "streamable-http" in result


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "ftp://example.com/mcp",
        "http:///mcp",
        "http://example.com:99999",
        "http://user:secret@example.com",
        "http://example.com/#x",
        "http://exa mple.com",
        "http://example.com\\mcp",
        "http://%",
        "http://example.com:",
        "http://example.com/#",
        "http://example.com../mcp",
        "http://example.com/\x7f",
        "http://example.com/\x80",
    ],
)
def test_http_config_rejects_invalid_urls(url):
    with pytest.raises(ValueError, match="http/https"):
        generate_http_config(url)


@pytest.mark.parametrize(
    "url", ["http://127.0.0.1:8000/mcp", "https://example.com/custom-mcp", "http://[::1]:8000/mcp"]
)
def test_http_config_accepts_valid_endpoints_without_connecting(url):
    assert (
        json.loads(generate_http_config(url))["mcpServers"]["learn-mcp-server-http"]["url"] == url
    )


def test_levels_have_distinct_exercises_and_unknown_level_is_rejected():
    plans = [generate_learning_plan(level) for level in ("beginner", "intermediate", "advanced")]
    assert len({plan.split("\n", 1)[1] for plan in plans}) == 3
    assert "divide" in plans[0] and "进度" in plans[1] and "MRTR" in plans[2]
    with pytest.raises(ValueError, match="level 不支持"):
        generate_learning_plan("unknown")


@pytest.mark.parametrize("answer", ["tool", "Tool 不是模型调用的动作，也不能用 @mcp.tool 注册。"])
def test_keyword_feedback_does_not_claim_correctness(answer):
    result = check_answer("tool", answer)
    assert "不是语义判卷" in result
    assert "答得不错" not in result
    assert "不能证明观点正确" in result


def test_learning_route_has_valid_targets_and_completion():
    assert set(LEARNING_SEQUENCE) <= CONCEPTS.keys()
    assert set(CONCEPTS) == set(TOPIC_SOURCES)
    assert {topic for module in LEARNING_MODULES for topic in module["topics"]} <= CONCEPTS.keys()
    assert "推荐下一步：tests" in suggest_next_step("debug")
    assert "已完成" in suggest_next_step("tests")
    assert "推荐下一步：tool" not in suggest_next_step("unknown")


@pytest.mark.parametrize(
    "text", ["FastMCP HTTP connection refused", "ConnectError: connection refused"]
)
def test_connection_evidence_wins_over_framework_name(text):
    assert "HTTP 连接" in diagnose_issue(text)
    assert "依赖" not in diagnose_issue(text)


def test_stdout_json_error_is_not_configuration_error():
    result = explain_error_message("stdio stdout JSON decode error: Expecting value")
    assert "stdio 协议" in result and "stderr" in result
    assert "候选判断：配置" not in result
    assert "信息不足" in diagnose_issue("FastMCP 好像有点问题")


def test_actual_import_error_wins_over_stdio_context():
    result = diagnose_issue("stdio 子进程启动失败：ModuleNotFoundError: No module named fastmcp")
    assert "依赖或解释器环境" in result
    assert "stdio 协议输出问题" not in result


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({"type": "http", "command": "python"}, "配置错误"),
        ({"type": "stdio", "url": "http://localhost/mcp"}, "配置错误"),
        ({"type": None, "command": "python"}, "配置错误"),
        ({"type": 1, "command": "python"}, "配置错误"),
        ({"type": "sse", "url": "http://localhost/sse"}, "旧 HTTP+SSE"),
        ({"type": "host-specific", "url": "http://localhost/mcp"}, "支持范围"),
    ],
)
def test_explicit_transport_type_is_not_silently_ignored(config, expected):
    assert expected in explain_config(json.dumps({"mcpServers": {"learn": config}}))


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("HTTP 404 Not Found", "HTTP 连接"),
        ("错误代码 4044", "信息不足"),
        ("stdio 启动出现 JSON 配置错误", "配置 JSON"),
        ("schema 中包含 print 字段", "信息不足"),
        ("security 问题", "信息不足"),
        ("ImportError: cannot import name 'REQUEST_TIMEOUT' from 'mcp_types'", "依赖或解释器环境"),
        ("httpx2.ReadTimeout: request timed out", "HTTP 连接"),
        ("Tool JSON 返回解析失败", "需区分配置与协议结果"),
    ],
)
def test_debug_rules_require_specific_evidence(text, expected):
    assert expected in diagnose_issue(text)


@pytest.mark.parametrize("days", [0, -1, 31, 1000000, True, 1.5])
def test_prompt_days_business_range(days):
    with pytest.raises(ValueError, match="days"):
        generate_mcp_study_plan("beginner", days)


def test_prompt_valid_days_and_blank_code():
    assert "30 天" in generate_mcp_study_plan("advanced", 30)
    with pytest.raises(ValueError, match="code 不能为空"):
        review_mcp_code("  ")


@pytest.mark.parametrize("value", ["0", "65536", "invalid"])
def test_http_port_invalid_values(monkeypatch, value):
    monkeypatch.setenv("LEARN_MCP_HTTP_PORT", value)
    with pytest.raises(ValueError, match="LEARN_MCP_HTTP_PORT"):
        get_http_port()
