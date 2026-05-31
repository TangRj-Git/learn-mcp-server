from learn_mcp_server.data.configs import DEBUG_GUIDES
from learn_mcp_server.utils import normalize_key, require_not_blank


def diagnose_issue(issue_description: str) -> str:
    """
    根据问题描述给出 MCP 调试建议。
    """
    normalized_issue = normalize_key(require_not_blank(issue_description, "issue_description"))

    if "stdio" in normalized_issue or "print" in normalized_issue:
        return """
# stdio 问题诊断

你描述的问题很可能和 stdio 输出有关。

建议检查：

1. stdio 模式下不要使用 print 输出普通日志
2. stdout 是 MCP 协议通道
3. 普通日志应写入 stderr 或日志文件
4. 确认 Host 启动的是正确的 Python 虚拟环境
"""

    if "module" in normalized_issue or "fastmcp" in normalized_issue or "import" in normalized_issue:
        return """
# 依赖问题诊断

你描述的问题很可能和 uv/uvx 运行环境或依赖解析有关。

建议检查：

1. 用户机器是否已经安装 uv。
2. Host 配置中的 command 是否是 uvx，args 是否包含 --from 和 learn-mcp-server。
3. 如果是本地开发配置，确认使用 uv run --directory 指向项目根目录。
4. 执行 uv run python -c "import fastmcp" 确认依赖能被 uv 环境解析。
"""

    if "resource" in normalized_issue or "uri" in normalized_issue:
        return """
# Resource 问题诊断

你描述的问题可能和 Resource URI 或注册有关。

建议检查：

1. URI 是否和 @mcp.resource() 中完全一致
2. Resource Template 参数名是否和 URI 占位符一致
3. Inspector 中是否能看到对应 Resource
"""

    return DEBUG_GUIDES["common-errors"].strip()


def list_common_errors() -> str:
    """
    列出 MCP 项目常见错误。
    """
    return DEBUG_GUIDES["common-errors"].strip()


def explain_error_message(error_text: str) -> str:
    """
    解释一段常见 MCP 或 Python 错误消息，并给出排查方向。
    """
    normalized_error = require_not_blank(error_text, "error_text")
    lowered_error = normalized_error.lower()

    if "modulenotfounderror" in lowered_error or "no module named" in lowered_error:
        diagnosis = "这通常是 uv/uvx 环境、包名版本或依赖解析问题。"
        next_actions = [
            "确认 Host 配置里的 command 使用 uvx。",
            "确认 args 中包含 --from 和 learn-mcp-server==0.1.0。",
            "如果是本地开发运行，执行 uv run python -c \"import fastmcp\" 检查依赖。",
        ]
    elif "json" in lowered_error or "expecting" in lowered_error:
        diagnosis = "这通常是 JSON 配置格式问题。"
        next_actions = [
            "检查配置文件是否有多余逗号、缺少引号或括号不闭合。",
            "确认顶层包含 mcpServers 字段。",
            "可以把配置传给 explain_config 继续分析。",
        ]
    elif "connection" in lowered_error or "refused" in lowered_error or "404" in lowered_error:
        diagnosis = "这通常是 streamable-http 连接或地址问题。"
        next_actions = [
            "确认 MCP Server 已经以 streamable-http 方式启动。",
            "确认 URL 指向 /mcp。",
            "检查端口是否被占用或被防火墙拦截。",
        ]
    elif "stdio" in lowered_error or "stdout" in lowered_error or "print" in lowered_error:
        diagnosis = "这通常是 stdio 协议通道被普通输出污染。"
        next_actions = [
            "不要在 stdio 模式下用 print 输出普通日志。",
            "普通日志写入 stderr 或日志文件。",
            "用 Inspector 重新启动服务后再查看工具列表。",
        ]
    else:
        diagnosis = "这看起来是通用 MCP 调试问题，需要先定位发生在启动、配置、注册还是调用阶段。"
        next_actions = [
            "确认服务能启动。",
            "确认 Host 配置正确。",
            "确认工具、资源或 Prompt 已经注册。",
            "再用 diagnose_issue 描述现象获取更具体建议。",
        ]

    lines = [
        "# 错误消息解释",
        "",
        "原始错误：",
        "",
        normalized_error,
        "",
        "判断：",
        diagnosis,
        "",
        "建议排查：",
    ]
    lines.extend(f"{index}. {action}" for index, action in enumerate(next_actions, start=1))
    return "\n".join(lines)


__all__ = ["diagnose_issue", "explain_error_message", "list_common_errors"]
