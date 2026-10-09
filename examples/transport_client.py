"""真实 stdio/HTTP Client；HTTP 模式连接已运行的本地服务。"""

import argparse
import asyncio
import json
import math
import sys
from pathlib import Path

from client_test import check_connection
from fastmcp import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport


async def main(transport_name: str, url: str, timeout: float, mode: str = "auto") -> None:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout 必须是有限正数。")
    if transport_name == "stdio":
        transport = StdioTransport(
            command=sys.executable,
            args=["-m", "learn_mcp_server.server"],
            cwd=str(Path(__file__).resolve().parents[1]),
            env={"LEARN_MCP_TRANSPORT": "stdio", "PYTHONIOENCODING": "utf-8"},
            keep_alive=False,
        )
    else:
        transport = StreamableHttpTransport(url=url)
    async with Client(transport, timeout=timeout, mode=mode) as client:
        result = await check_connection(client)
    print(json.dumps({"transport": transport_name, **result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transport", choices=["stdio", "http"])
    parser.add_argument("--url", default="http://127.0.0.1:8000/mcp")
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--mode", choices=["auto", "2026-07-28", "legacy"], default="auto")
    args = parser.parse_args()
    asyncio.run(main(args.transport, args.url, args.timeout, args.mode))
