"""真实子进程/HTTP 冒烟：验证入口、协议通道与 Origin 防护。"""

import asyncio
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx2
import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from learn_mcp_server import __version__
from learn_mcp_server.settings import PROTOCOL_REVISION

ROOT = Path(__file__).resolve().parents[1]


async def check_usage(client, revision=PROTOCOL_REVISION):
    assert client.protocol_version == revision
    assert "get_server_info" in {tool.name for tool in await client.list_tools()}
    result = await client.call_tool("explain_concept", {"concept": "tool"})
    assert "model-controlled" in result.data
    resource = (await client.read_resource("mcp://concepts/TOOL"))[0]
    assert resource.mime_type == "text/markdown"
    prompt = await client.get_prompt("generate_mcp_study_plan", {"level": "beginner", "days": "3"})
    assert "3 天" in prompt.messages[0].content.text


@pytest.mark.parametrize(
    ("mode", "revision"),
    [("auto", PROTOCOL_REVISION), (PROTOCOL_REVISION, PROTOCOL_REVISION), ("legacy", "2025-11-25")],
)
def test_real_stdio_subprocess(mode, revision):
    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "learn_mcp_server.server"],
        cwd=str(ROOT),
        env={"LEARN_MCP_TRANSPORT": "stdio", "PYTHONIOENCODING": "utf-8"},
        keep_alive=False,
    )

    async def check():
        async with Client(transport, timeout=10, init_timeout=10, mode=mode) as client:
            await check_usage(client, revision)

    asyncio.run(check())


@pytest.fixture(scope="module")
def http_server(tmp_path_factory):
    with socket.socket() as bound:
        bound.bind(("127.0.0.1", 0))
        port = bound.getsockname()[1]
    log_path = tmp_path_factory.mktemp("http-server") / "server.log"
    env = {
        **os.environ,
        "LEARN_MCP_TRANSPORT": "streamable-http",
        "LEARN_MCP_HTTP_PORT": str(port),
        "PYTHONIOENCODING": "utf-8",
    }
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", "learn_mcp_server.server"],
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            deadline = time.monotonic() + 12
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    pytest.fail(log_path.read_text(encoding="utf-8"))
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                        break
                except OSError:
                    time.sleep(0.05)
            else:
                pytest.fail("本地 HTTP 服务未在 12 秒内就绪。")
            yield f"http://127.0.0.1:{port}/mcp"
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


@pytest.mark.parametrize(
    ("mode", "revision"),
    [("auto", PROTOCOL_REVISION), (PROTOCOL_REVISION, PROTOCOL_REVISION), ("legacy", "2025-11-25")],
)
def test_real_http_client(http_server, monkeypatch, mode, revision):
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost,::1")

    async def check():
        async with Client(http_server, timeout=10, init_timeout=10, mode=mode) as client:
            await check_usage(client, revision)

    asyncio.run(check())


@pytest.mark.parametrize(
    "origin", ["https://unrelated.example", "http://127.0.0.1.evil.example", "null"]
)
def test_http_invalid_origin_is_rejected_before_mcp(http_server, origin):
    with httpx2.Client(trust_env=False, timeout=5) as client:
        response = client.post(http_server, headers={"Origin": origin}, json={})
    assert response.status_code == 403


def test_http_foreign_host_is_rejected(http_server):
    with httpx2.Client(trust_env=False, timeout=5) as client:
        response = client.post(http_server, headers={"Host": "unrelated.example"}, json={})
    assert response.status_code == 421


@pytest.mark.parametrize("origin", [None, "http://localhost:6274"])
def test_http_legacy_initialize_compatibility(http_server, origin):
    headers = {"Accept": "application/json, text/event-stream"}
    if origin is not None:
        headers["Origin"] = origin
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "learning-test", "version": "1"},
        },
    }
    with httpx2.Client(trust_env=False, timeout=5) as client:
        response = client.post(http_server, headers=headers, json=payload)
    assert response.status_code == 200
    text = next(
        (line[6:] for line in response.text.splitlines() if line.startswith("data: ")),
        response.text,
    )
    result = json.loads(text)["result"]
    assert result["serverInfo"]["version"] == __version__
    assert result["protocolVersion"] == "2025-11-25"


def test_http_modern_metadata_discovery_and_call_without_handshake(http_server):
    metadata = {
        "io.modelcontextprotocol/protocolVersion": PROTOCOL_REVISION,
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {"name": "modern-learning-test", "version": "1"},
    }

    def post(client, method, params):
        headers = {
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL_REVISION,
            "MCP-Method": method,
        }
        if method in {"tools/call", "prompts/get", "resources/read"}:
            headers["Mcp-Name"] = params.get("name", params.get("uri"))
        response = client.post(
            http_server,
            headers=headers,
            json={
                "jsonrpc": "2.0",
                "id": method,
                "method": method,
                "params": {"_meta": metadata, **params},
            },
        )
        assert response.status_code == 200, response.text
        assert "mcp-session-id" not in response.headers
        body = next(
            (line[6:] for line in response.text.splitlines() if line.startswith("data: ")),
            response.text,
        )
        return json.loads(body)["result"]

    with httpx2.Client(trust_env=False, timeout=5) as client:
        discovery = post(client, "server/discover", {})
        assert discovery["resultType"] == "complete"
        assert PROTOCOL_REVISION in discovery["supportedVersions"]
        assert discovery["_meta"]["io.modelcontextprotocol/serverInfo"]["version"] == __version__
        for method, params in [
            ("server/discover", {}),
            ("tools/list", {}),
            ("resources/list", {}),
            ("resources/templates/list", {}),
            ("prompts/list", {}),
            ("resources/read", {"uri": "mcp://docs/introduction"}),
        ]:
            cached_result = (
                discovery if method == "server/discover" else post(client, method, params)
            )
            assert cached_result["resultType"] == "complete"
            assert cached_result["ttlMs"] >= 0
            assert cached_result["cacheScope"] in {"public", "private"}
        result = post(client, "tools/call", {"name": "get_server_info", "arguments": {}})
        assert result["resultType"] == "complete" and result["isError"] is False
        assert "FastMCP 4.x" in result["content"][0]["text"]


def test_http_modern_mismatched_tool_header_returns_protocol_error(http_server):
    with httpx2.Client(trust_env=False, timeout=5) as client:
        response = client.post(
            http_server,
            headers={
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": PROTOCOL_REVISION,
                "Mcp-Method": "tools/call",
                "Mcp-Name": "wrong_tool",
            },
            json={
                "jsonrpc": "2.0",
                "id": "header-mismatch",
                "method": "tools/call",
                "params": {
                    "name": "get_server_info",
                    "arguments": {},
                    "_meta": {
                        "io.modelcontextprotocol/protocolVersion": PROTOCOL_REVISION,
                        "io.modelcontextprotocol/clientCapabilities": {},
                    },
                },
            },
        )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == -32020
