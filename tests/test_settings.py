import pytest

from learn_mcp_server.settings import get_transport


def test_get_transport_defaults_to_stdio(monkeypatch):
    monkeypatch.delenv("LEARN_MCP_TRANSPORT", raising=False)

    assert get_transport() == "stdio"


def test_get_transport_reads_streamable_http_from_env(monkeypatch):
    monkeypatch.setenv("LEARN_MCP_TRANSPORT", "streamable-http")

    assert get_transport() == "streamable-http"


def test_get_transport_rejects_unknown_transport(monkeypatch):
    monkeypatch.setenv("LEARN_MCP_TRANSPORT", "websocket")

    with pytest.raises(ValueError, match="不支持的 transport"):
        get_transport()
