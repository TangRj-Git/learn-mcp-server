import json

from learn_mcp_server.settings import PROJECT_NAME
from learn_mcp_server.utils import require_http_url, require_not_blank, require_string_list


def explain_config(config_text: str) -> str:
    """
    解释生态常见的 mcpServers JSON 配置；不解析所有 Host 的专属格式，不执行命令。
    """
    stripped_config = require_not_blank(config_text, "config_text")

    try:
        config = json.loads(stripped_config)
    except json.JSONDecodeError as error:
        return f"这不是合法的 JSON 配置：{error.msg}"

    if not isinstance(config, dict):
        return "配置根必须是 JSON 对象，不能是数组、null 或标量。"
    mcp_servers = config.get("mcpServers")
    if not isinstance(mcp_servers, dict):
        return "mcpServers 必须是对象；请确认该 Host 使用 mcpServers JSON 格式。"

    if not mcp_servers:
        return "mcpServers 是空对象，没有可解释的 Server 配置。"

    lines = ["# MCP 配置解释", ""]
    for server_name, server_config in mcp_servers.items():
        lines.append(f"## {server_name}")
        if not isinstance(server_config, dict):
            lines.append("这个 Server 配置不是对象，建议检查格式。")
            lines.append("")
            continue

        if "command" in server_config and "url" in server_config:
            lines.append("配置冲突：当前格式中的 command 与 url 不应同时存在。")
            lines.append("")
            continue

        try:
            transport_type = server_config.get("type")
            if "type" in server_config:
                if not isinstance(transport_type, str):
                    raise ValueError("type 必须是字符串。")
                transport_type = require_not_blank(transport_type, "type").lower()
                if transport_type not in {"stdio", "http", "streamable-http", "sse"}:
                    lines.append("该 Host 的 type 值不在本讲解器支持范围，请核对其产品文档。")
                    lines.append("")
                    continue
                expected_field = "command" if transport_type == "stdio" else "url"
                if expected_field not in server_config:
                    raise ValueError(f"type={transport_type} 应使用 {expected_field} 字段。")
            if "command" in server_config:
                command = require_not_blank(server_config["command"], "command")
                args = require_string_list(server_config.get("args", []), "args")
                env = server_config.get("env", {})
                if not isinstance(env, dict) or any(
                    not isinstance(value, str) for value in env.values()
                ):
                    raise ValueError("env 必须是字符串值组成的对象。")
            elif "url" in server_config:
                url = require_http_url(server_config["url"], "url")
                if "args" in server_config or "env" in server_config:
                    raise ValueError("HTTP 配置不应包含本地进程的 args/env。")
        except ValueError as error:
            lines.append(f"配置错误：{error}")
            lines.append("")
            continue

        if "command" in server_config:
            lines.append("这是一个 stdio 配置。")
            lines.append(f"command: {command}")
            lines.append(f"args: {len(args)} 个参数（值已省略，避免回显凭证）。")
            if env:
                lines.append(f"env: {', '.join(env)}（值已隐藏）。")
            lines.append("有效的 python/node/二进制命令均可使用；uv/uvx 是本项目推荐方式。")
        elif "url" in server_config:
            if transport_type == "sse":
                lines.append("这是旧 HTTP+SSE 传输配置；本项目只提供 stdio 与 streamable-http。")
            else:
                lines.append("这是一个 streamable-http 配置。")
            parts = url.split("?", 1)
            lines.append(f"url: {parts[0]}" + ("?（查询参数已隐藏）" if len(parts) > 1 else ""))
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
    normalized_url = require_http_url(server_url)

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
- 常见问题是服务没启动、端口不通、URL 与实际 endpoint 不符；本项目默认 /mcp。

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
