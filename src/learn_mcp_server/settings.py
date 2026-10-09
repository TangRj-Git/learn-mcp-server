"""环境变量和运行常量；配置读取不负责启动服务。"""

import os
from typing import Final, Literal, TypeAlias, cast

PROJECT_NAME: Final = "learn-mcp-server"

Transport: TypeAlias = Literal["stdio", "streamable-http"]

DEFAULT_TRANSPORT: Final[Transport] = "stdio"
VALID_TRANSPORTS: Final[tuple[Transport, ...]] = ("stdio", "streamable-http")
PROTOCOL_REVISION: Final = "2026-07-28"
HTTP_HOST: Final = "127.0.0.1"


def get_transport() -> Transport:
    """
    获取当前 Server 运行 transport。
    """
    transport = os.getenv("LEARN_MCP_TRANSPORT", DEFAULT_TRANSPORT).strip().lower()

    if transport not in VALID_TRANSPORTS:
        available_transports = ", ".join(sorted(VALID_TRANSPORTS))
        raise ValueError(f"不支持的 transport：{transport}。可用值：{available_transports}")

    return cast(Transport, transport)


def get_http_port() -> int:
    """读取本地 HTTP 端口；默认 8000，不开放外网监听。"""
    try:
        port = int(os.getenv("LEARN_MCP_HTTP_PORT", "8000"))
    except ValueError as error:
        raise ValueError("LEARN_MCP_HTTP_PORT 必须是 1–65535 的整数。") from error
    if not 1 <= port <= 65535:
        raise ValueError("LEARN_MCP_HTTP_PORT 必须是 1–65535 的整数。")
    return port


__all__ = [
    "DEFAULT_TRANSPORT",
    "HTTP_HOST",
    "PROJECT_NAME",
    "PROTOCOL_REVISION",
    "VALID_TRANSPORTS",
    "Transport",
    "get_http_port",
    "get_transport",
]
