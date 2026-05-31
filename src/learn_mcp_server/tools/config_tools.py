import json

from learn_mcp_server.settings import PROJECT_NAME
from learn_mcp_server.utils import require_not_blank, require_string_list


def explain_config(config_text: str) -> str:
    """
    解释 MCP Host 配置文本。
    """
    stripped_config = require_not_blank(config_text, "config_text")

    try:
        config = json.loads(stripped_config)
    except json.JSONDecodeError as error:
        return f"这不是合法的 JSON 配置：{error.msg}"

    mcp_servers = config.get("mcpServers")
    if not isinstance(mcp_servers, dict):
        return "这个配置没有找到 mcpServers 字段，请确认它是不是 MCP Host 配置。"

    lines = ["# MCP 配置解释", ""]
    for server_name, server_config in mcp_servers.items():
        lines.append(f"## {server_name}")
        if not isinstance(server_config, dict):
            lines.append("这个 Server 配置不是对象，建议检查格式。")
            lines.append("")
            continue

        if "command" in server_config:
            lines.append("这是一个 stdio 配置。")
            lines.append(f"command: {server_config.get('command')}")
            lines.append(f"args: {server_config.get('args', [])}")
        elif "url" in server_config:
            lines.append("这是一个 streamable-http 配置。")
            lines.append(f"url: {server_config.get('url')}")
        else:
            lines.append("没有看到 command 或 url，无法判断 transport 类型。")
        lines.append("")

    return "\n".join(lines)


def generate_stdio_config(command: str, args: list[str]) -> str:
    """
    生成本地 stdio MCP Host 配置。
    """
    normalized_command = require_not_blank(command, "command")
    normalized_args = require_string_list(args, "args")

    config = {
        "mcpServers": {
            PROJECT_NAME: {
                "command": normalized_command,
                "args": normalized_args,
            }
        }
    }
    return json.dumps(config, ensure_ascii=False, indent=2)


def generate_http_config(server_url: str) -> str:
    """
    生成 streamable-http MCP Host 配置。
    """
    normalized_url = require_not_blank(server_url, "server_url")

    config = {
        "mcpServers": {
            f"{PROJECT_NAME}-http": {
                "url": normalized_url,
            }
        }
    }
    return json.dumps(config, ensure_ascii=False, indent=2)


def compare_local_and_remote_config() -> str:
    """
    对比本地 stdio 配置和远程 streamable-http 配置。
    """
    return """
# 本地配置和远程配置对比

## 本地 stdio 配置

- 由 Host 启动 MCP Server 进程。
- 配置重点是 command 和 args。
- 给别人使用时推荐 command 使用 uvx，并通过 --from 指定包名和版本。
- 本地开发时推荐 command 使用 uv，并通过 run --directory 指向项目目录。
- 常见问题是 uv 未安装、uvx 包名或版本不对、uv run --directory 路径不对、stdout 被普通日志污染。

## 远程或 HTTP 配置

- MCP Server 需要提前运行。
- 配置重点是 url。
- 适合长期运行、跨进程访问、跨机器访问或 Web 服务形态。
- 常见问题是服务没启动、端口不通、URL 没有指向 /mcp。

## 选择建议

学习和本地调试优先使用 stdio。
需要让多个 Host 或远程客户端访问时，再考虑 streamable-http。
""".strip()


__all__ = [
    "compare_local_and_remote_config",
    "explain_config",
    "generate_http_config",
    "generate_stdio_config",
]
