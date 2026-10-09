"""主服务入口：创建实例、显式注册并按配置启动。"""

from fastmcp import FastMCP

from learn_mcp_server import __version__
from learn_mcp_server.data.references import BASELINE
from learn_mcp_server.registry import register_all
from learn_mcp_server.settings import HTTP_HOST, PROJECT_NAME, get_http_port, get_transport


def create_server() -> FastMCP:
    """
    创建并注册 learn-mcp-server 的 MCP 能力。
    """
    server = FastMCP(
        PROJECT_NAME,
        version=__version__,
        instructions="用于学习 MCP：用 Tool 查询和自查，用 Resource 读取资料，用 Prompt 获取消息模板。"
        f"主课程基线：{BASELINE}；旧握手仅作为历史对照，可选能力不等于本项目已实现。",
    )
    register_all(server)
    return server


mcp = create_server()


def main() -> None:
    """
    命令行入口。
    """
    transport = get_transport()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(
            transport="streamable-http",
            host=HTTP_HOST,
            port=get_http_port(),
            host_origin_protection=True,
        )


if __name__ == "__main__":
    main()
