"""复验 Client 模式与现代 HTTP；新记录默认写入 artifacts/runtime。"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx2

from learn_mcp_server.settings import PROTOCOL_REVISION

ROOT = Path(__file__).resolve().parents[1]
ENV = {
    **os.environ,
    "PYTHONIOENCODING": "utf-8",
    "FASTMCP_MCP_CAMELCASE_COMPAT": "false",
    "NO_PROXY": "127.0.0.1,localhost,::1",
}
MODES = {"auto": PROTOCOL_REVISION, PROTOCOL_REVISION: PROTOCOL_REVISION, "legacy": "2025-11-25"}


def check_cli(arguments: list[str]) -> dict:
    """运行现有教学 Client，验证协议、能力数量与实际 MIME。"""
    result = subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        env=ENV,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=25,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
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
    return {"command": arguments, "result": data}


def check_http(output: Path, observations: list[dict]) -> int:
    """启动临时本地 HTTP 服务、保存原始报文，并清理子进程。"""
    with socket.socket() as bound:
        bound.bind(("127.0.0.1", 0))
        port = bound.getsockname()[1]
    url = f"http://127.0.0.1:{port}/mcp"
    with (output / "http-server.log").open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", "learn_mcp_server.server"],
            cwd=ROOT,
            env={
                **ENV,
                "LEARN_MCP_TRANSPORT": "streamable-http",
                "LEARN_MCP_HTTP_PORT": str(port),
            },
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
                observations.append(
                    check_cli(
                        ["examples/transport_client.py", "http", "--url", url, "--mode", mode]
                    )
                )
            metadata = {
                "io.modelcontextprotocol/protocolVersion": PROTOCOL_REVISION,
                "io.modelcontextprotocol/clientCapabilities": {},
                "io.modelcontextprotocol/clientInfo": {"name": "runtime-check", "version": "1"},
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
                        "MCP-Protocol-Version": PROTOCOL_REVISION,
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
                        (
                            line[6:]
                            for line in response.text.splitlines()
                            if line.startswith("data: ")
                        ),
                        response.text,
                    )
                    body = json.loads(body)
                    assert body["result"]["resultType"] == "complete"
                    wire.append({"request_headers": headers, "request": payload, "response": body})
            (output / "modern-wire.json").write_text(
                json.dumps(wire, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
    return len(wire)


def main(output: Path) -> None:
    """复用 examples 中的入口；可导入本脚本而不启动检查。"""
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    observations = []
    for mode in MODES:
        observations.append(check_cli(["examples/client_test.py", "--mode", mode]))
        observations.append(check_cli(["examples/transport_client.py", "stdio", "--mode", mode]))
    for mode in ("auto", "legacy"):
        observations.append(check_cli(["examples/client_test.py", "--demo", "--mode", mode]))
    wire_cases = check_http(output, observations)
    (output / "cli-runtime.json").write_text(
        json.dumps(observations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "cli_cases": len(observations),
                "wire_cases": wire_cases,
                "cleanup": "passed",
                "output_directory": str(output),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "artifacts" / "runtime")
    args = parser.parse_args()
    main(args.output_dir)
