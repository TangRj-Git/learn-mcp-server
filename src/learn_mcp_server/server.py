from fastmcp import FastMCP

from learn_mcp_server.registry import register_all
from learn_mcp_server.settings import PROJECT_NAME, get_transport


def create_server() -> FastMCP:
    """
    创建并注册 learn-mcp-server 的 MCP 能力。
    """
    server = FastMCP(PROJECT_NAME)
    globals().update(register_all(server))
    return server


mcp = create_server()


def main() -> None:
    """
    命令行入口。
    """
    mcp.run(transport=get_transport())


if __name__ == "__main__":
    main()
