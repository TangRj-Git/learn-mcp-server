import re

from learn_mcp_server.data.configs import DEBUG_GUIDES
from learn_mcp_server.utils import normalize_key, require_not_blank


def _diagnosis(text: str) -> tuple[str, list[str]]:
    """具体证据先于框架名；规则只提供排查方向，不自动执行。"""
    lowered = normalize_key(text)
    if any(
        term in lowered
        for term in ("modulenotfounderror", "no module named", "importerror", "cannot import")
    ):
        return "依赖或解释器环境问题", [
            "核对实际启动命令与解释器，Python/uv/uvx 均可使用。",
            "使用 uv 时确认 uv/uvx 已安装，包名和版本正确。",
            '本地开发确认 uv run --directory 指向项目；执行 uv run python -c "import fastmcp" 检查环境。',
        ]
    if re.search(r"\b404\b", lowered) or any(
        term in lowered
        for term in (
            "connection refused",
            "connecterror",
            "连接拒绝",
            "http timeout",
            "连接超时",
            "httpx.readtimeout",
            "httpx2.readtimeout",
        )
    ):
        return "HTTP 连接或端点问题", [
            "确认 Server 已独立启动，并核对实际监听端口。",
            "检查 URL 与服务 endpoint；本项目默认 /mcp。",
            "检查超时、代理、防火墙；用真实 HTTP Client 验证。",
        ]
    if "timeout" in lowered or "超时" in lowered:
        return "调用超时，需区分启动、连接与执行阶段", [
            "核对 Client 等待时限与服务是否在执行。",
            "检查是否有进度、取消与清理；超时不代表副作用已回滚。",
        ]
    if "stdout" in lowered or ("stdio" in lowered and "print" in lowered):
        return "stdio 协议输出问题", [
            "stdout 只写协议消息；不要使用 print 输出普通日志。",
            "普通日志写 stderr，检查子进程的启动与输出。",
            "用真实 stdio Client 重新发现能力；JSON 解析失败可能来自输出污染。",
        ]
    if re.search(r"\b(resources?|uri)\b", lowered) or "resourceerror" in lowered:
        return "Resource URI 或注册问题", [
            "比较 resources/list 与 resources/templates/list 的入口。",
            "URI 占位符须对应函数参数，读取时使用展开后的 URI。",
            "区分目标正文与未知主题帮助页。",
        ]
    if any(term in lowered for term in ("mcpservers", "配置", "config", "command", "args")):
        return "配置 JSON 或字段问题", [
            "检查对象根、括号、引号与逗号。",
            "确认该 Host 使用 mcpServers 格式；检查 command/args 与 url 冲突。",
            "调用 explain_config 做静态检查，不执行配置命令。",
        ]
    if "json" in lowered or "expecting" in lowered:
        return "JSON 结构错误，需区分配置与协议结果", [
            "确认错误来自 Host 配置、Tool 参数/结果还是 stdio 协议消息。",
            "检查原始结构与对应 schema；配置问题可使用 explain_config。",
        ]
    if "stdio" in lowered:
        return "stdio 进程或连接问题，证据不足", [
            "核对启动命令、工作目录、解释器和子进程 stderr。",
            "用真实 stdio Client 验证；出现具体错误后再定位输出、配置或依赖。",
        ]
    return "信息不足：需要定位失败层次", [
        "补充启动命令、传输模式、完整错误与失败步骤，隐藏凭证。",
        "先检查内存注册/API，再检查进程或网络，最后检查 Host 展示。",
        "仅出现 FastMCP 字样不能判定是依赖错误。",
    ]


def diagnose_issue(issue_description: str) -> str:
    """根据具体错误证据列出排查动作；没有证据时说明不确定性。"""
    text = require_not_blank(issue_description, "issue_description")
    category, actions = _diagnosis(text)
    return f"# {category}诊断\n\n这是候选排查方向，不自动执行命令。\n\n" + "\n".join(
        f"{index}. {action}" for index, action in enumerate(actions, 1)
    )


def list_common_errors() -> str:
    """读取本项目常见调试问题清单。"""
    return DEBUG_GUIDES["common-errors"].strip()


def explain_error_message(error_text: str) -> str:
    """解释错误并给出验证动作；不会根据单个框架名做确定性结论。"""
    text = require_not_blank(error_text, "error_text")
    category, actions = _diagnosis(text)
    return (
        "# 错误消息解释\n\n候选判断："
        + category
        + "\n\n建议排查：\n\n"
        + "\n".join(f"{index}. {action}" for index, action in enumerate(actions, 1))
    )


__all__ = ["diagnose_issue", "explain_error_message", "list_common_errors"]
