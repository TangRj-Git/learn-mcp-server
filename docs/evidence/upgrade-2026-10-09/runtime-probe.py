"""升级验收探针：源码工作区运行，结果写入本目录，不是 Server 的运行依赖。"""

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx2

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent
ENV = {
    **os.environ,
    "PYTHONIOENCODING": "utf-8",
    "FASTMCP_MCP_CAMELCASE_COMPAT": "false",
    "NO_PROXY": "127.0.0.1,localhost,::1",
}
MODES = {"auto": "2026-07-28", "2026-07-28": "2026-07-28", "legacy": "2025-11-25"}
observations = []


def check_cli(arguments):
    result = subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        env=ENV,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=25,
    )
    result.check_returncode()
    data = json.loads(result.stdout)
    mode = arguments[arguments.index("--mode") + 1]
    assert data["protocol_version"] == MODES[mode]
    expected = (2, 1, 1, 2) if "--demo" in arguments else (20, 39, 5, 5)
    assert (
        len(data["tools"]),
        data["resources"],
        len(data["resource_templates"]),
        len(data["prompts"]),
    ) == expected
    assert data["template_mime"] == "text/markdown"
    observations.append({"command": arguments, "result": data})


for mode in MODES:
    check_cli(["examples/client_test.py", "--mode", mode])
    check_cli(["examples/transport_client.py", "stdio", "--mode", mode])
check_cli(["examples/client_test.py", "--demo", "--mode", "auto"])
check_cli(["examples/client_test.py", "--demo", "--mode", "legacy"])

with socket.socket() as bound:
    bound.bind(("127.0.0.1", 0))
    port = bound.getsockname()[1]
url = f"http://127.0.0.1:{port}/mcp"
with (OUTPUT / "http-server.log").open("w", encoding="utf-8") as log:
    process = subprocess.Popen(
        [sys.executable, "-m", "learn_mcp_server.server"],
        cwd=ROOT,
        env={**ENV, "LEARN_MCP_TRANSPORT": "streamable-http", "LEARN_MCP_HTTP_PORT": str(port)},
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=log,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    try:
        deadline = time.monotonic() + 12
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("HTTP Server 提前退出，请读取 http-server.log。")
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.05)
        else:
            raise TimeoutError("HTTP Server 未就绪。")
        for mode in MODES:
            check_cli(["examples/transport_client.py", "http", "--url", url, "--mode", mode])
        metadata = {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {"name": "upgrade-probe", "version": "1"},
        }
        wire = []
        with httpx2.Client(trust_env=False, timeout=5) as client:
            for method, params in [
                ("server/discover", {}),
                ("tools/list", {}),
                ("resources/read", {"uri": "mcp://concepts/TOOL"}),
                ("tools/call", {"name": "get_server_info", "arguments": {}}),
            ]:
                headers = {
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2026-07-28",
                    "Mcp-Method": method,
                }
                if method == "resources/read":
                    headers["Mcp-Name"] = params["uri"]
                elif method == "tools/call":
                    headers["Mcp-Name"] = params["name"]
                payload = {
                    "jsonrpc": "2.0",
                    "id": method,
                    "method": method,
                    "params": {"_meta": metadata, **params},
                }
                response = client.post(url, headers=headers, json=payload)
                assert response.status_code == 200, response.text
                assert "mcp-session-id" not in response.headers
                body = next(
                    (line[6:] for line in response.text.splitlines() if line.startswith("data: ")),
                    response.text,
                )
                body = json.loads(body)
                assert body["result"]["resultType"] == "complete"
                wire.append({"request_headers": headers, "request": payload, "response": body})
        (OUTPUT / "modern-wire.json").write_text(
            json.dumps(wire, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

(OUTPUT / "cli-runtime.json").write_text(
    json.dumps(observations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"cli_cases": len(observations), "wire_cases": len(wire), "cleanup": "passed"}))
