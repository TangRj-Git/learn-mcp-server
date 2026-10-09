import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stdio_config_is_valid_json():
    config = json.loads((ROOT / "examples" / "stdio_config.json").read_text(encoding="utf-8"))

    server = config["mcpServers"]["learn-mcp-server"]
    assert server["command"] == "uvx"
    assert server["args"] == ["--from", "learn-mcp-server==0.1.0", "learn-mcp-server"]


def test_streamable_http_config_is_valid_json():
    config = json.loads(
        (ROOT / "examples" / "streamable_http_config.json").read_text(encoding="utf-8")
    )

    server = config["mcpServers"]["learn-mcp-server-http"]
    assert server["url"] == "http://127.0.0.1:8000/mcp"


def test_env_example_documents_supported_settings():
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")

    assert "LEARN_MCP_TRANSPORT=stdio" in env_example
    assert "streamable-http" in env_example


def test_client_test_script_is_valid_python():
    source = (ROOT / "examples" / "client_test.py").read_text(encoding="utf-8")

    ast.parse(source)
    assert "Client" in source
    assert "list_tools" in source
