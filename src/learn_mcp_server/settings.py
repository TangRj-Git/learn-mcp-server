import os
from typing import Final, Literal, TypeAlias, cast

PROJECT_NAME: Final = "learn-mcp-server"

Transport: TypeAlias = Literal["stdio", "streamable-http"]

DEFAULT_TRANSPORT: Final[Transport] = "stdio"
VALID_TRANSPORTS: Final[tuple[Transport, ...]] = ("stdio", "streamable-http")


def get_transport() -> Transport:
    """
    获取当前 Server 运行 transport。
    """
    transport = os.getenv("LEARN_MCP_TRANSPORT", DEFAULT_TRANSPORT).strip().lower()

    if transport not in VALID_TRANSPORTS:
        available_transports = ", ".join(sorted(VALID_TRANSPORTS))
        raise ValueError(f"不支持的 transport：{transport}。可用值：{available_transports}")

    return cast(Transport, transport)


__all__ = ["PROJECT_NAME", "DEFAULT_TRANSPORT", "VALID_TRANSPORTS", "Transport", "get_transport"]
