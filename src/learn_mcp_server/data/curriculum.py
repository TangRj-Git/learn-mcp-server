"""课程、日计划和衔接共用的简单数据表。"""

from learn_mcp_server.data.references import BASELINE

LEARNING_LEVELS = ("beginner", "intermediate", "advanced")
LEVEL_TITLES = {"beginner": "入门", "intermediate": "进阶", "advanced": "高级"}
LEARNING_SEQUENCE = (
    "mcp",
    "host",
    "client",
    "server",
    "tool",
    "resource",
    "resource-template",
    "prompt",
    "schema",
    "structured-output",
    "errors",
    "transport",
    "stdio",
    "streamable-http",
    "config",
    "debug",
    "tests",
)

# 标题、目标、操作、验收。普通静态数据，无状态或课程引擎。
COURSE_LESSONS: dict[str, list[tuple[str, str, str, str]]] = {
    "beginner": [
        (
            "协议与角色",
            "区分 MCP、FastMCP、Host、Client、Server。",
            "读取 mcp://docs/introduction 与 mcp://docs/host-client-server。",
            "画出 Host → Client → Server，指出模型不是 Server。",
        ),
        (
            "最小 Tool",
            "发现并调用计算动作。",
            "运行 examples/minimal_server.py，用 examples/client_test.py --demo 检查。",
            "看到 divide 的 schema 并得到结构化 value。",
        ),
        (
            "Resource 与模板",
            "区分列表元数据和正文。",
            "读取 demo://metadata 与 demo://topics/tool，比较两个主题。",
            "JSON 能解析，Markdown 内容实际 MIME 正确。",
        ),
        (
            "Prompt",
            "获取消息模板而不执行模型。",
            "获取 explain_topic，观察 user/assistant 两条消息。",
            "解释 Prompt 参数在线上是字符串。",
        ),
        (
            "Inspector 与 stdio",
            "从独立进程检查通信。",
            "运行 examples/transport_client.py stdio；Inspector 使用绝对正斜杠路径与 :mcp、--no-reload。",
            "子进程可发现能力，stdout 只有协议，退出能清理。",
        ),
        (
            "自查与测试",
            "建立学习反馈的边界。",
            "get_practice_task('tool')；关键词自查后运行 uv run --locked pytest。",
            "不把 check_answer 当语义判卷，能解释验证结果。",
        ),
    ],
    "intermediate": [
        (
            "schema",
            "理解必需、默认、enum、说明与业务限制。",
            "读 mcp://concepts/schema 和 mcp://examples/schema；给 divide 传合法与非法参数。",
            "inputSchema 与错误状态符合声明。",
        ),
        (
            "结构化结果与错误",
            "区分 Python、wire 和 Client 对象。",
            "比较成功 value、is_error、ToolError 与未知工具错误。",
            "说明 content、structuredContent、outputSchema、result.data。",
        ),
        (
            "Resource Template 与 MIME",
            "处理可选查询参数。",
            "读取 demo://topics/tool?detail=true；读 mcp://concepts/resource-template。",
            "参数名对应签名；read 的 MIME 与实际正文匹配。",
        ),
        (
            "Prompt 参数",
            "观察字符串转换及多消息。",
            "get_prompt('study_plan', {'days': '3'})，再传越界天数。",
            "有效参数形成 messages，越界反馈可理解。",
        ),
        (
            "真实传输",
            "stdio 与 HTTP 生命周期。",
            "启动本地 HTTP，运行 transport_client.py http --url http://127.0.0.1:8000/mcp。",
            "可调用、读取、取 Prompt；无效 Origin 被拒绝。",
        ),
        (
            "Context 与进度",
            "注入 Context 并接收进度。",
            "在 demo Client 调用 count_steps，用 progress_handler 收集事件。",
            "ctx 不在 inputSchema，progress 为 1、2、3。",
        ),
        (
            "测试和包",
            "区分内存、真实传输和 wheel 验证。",
            "阅读 mcp://concepts/tests；uv build；项目外安装 wheel。",
            "包在没有仓库 examples/docs 的环境仍提供学习资料。",
        ),
    ],
    "advanced": [
        (
            "版本演进",
            "区分 2025-11-25 与 2026-07-28。",
            "读 mcp://concepts/latest-protocol、discovery，比较 initialize 和 server/discover。",
            "记录 Client 的 protocol_version，区分默认 modern 与显式 legacy。",
        ),
        (
            "MRTR",
            "理解补充输入和重试。",
            "读 mcp://concepts/mrtr，画 input_required → 新 id 重试 → complete。",
            "不解析 requestState，不手写 SDK 兼容层。",
        ),
        (
            "订阅和缓存",
            "理解通知、listen、ttlMs/cacheScope、cursor。",
            "读 subscriptions、caching、pagination、completion。",
            "缓存不是授权，参数补全不是文本生成。",
        ),
        (
            "边界和授权",
            "区分用户确认、Origin、OAuth、OS 权限。",
            "读 security、authorization、roots，完成 security 练习。",
            "知道 roots/uvx 不提供文件沙箱，表单不收集秘密。",
        ),
        (
            "历史能力与扩展",
            "理解弃用不等于移除。",
            "读 sampling、logging、tasks、apps、skills。",
            "Tasks 的旧核心与新扩展区分清楚，无需为学习服务增加队列。",
        ),
        (
            "迁移验证",
            "核对 FastMCP 4 主课程与版本维护。",
            "按 docs/protocol-versions.md 检查正常安装、原生属性、modern/legacy 与真实传输。",
            "无兼容弃用警告；不复制未经验证的 API。",
        ),
    ],
}


def _course(level: str, *, plan: bool = False) -> str:
    title = f"MCP {LEVEL_TITLES[level]}学习计划" if plan else f"MCP {level.title()} 课程"
    lines = [
        f"# {title}",
        "",
        f"运行基线：{BASELINE}。旧握手作为历史对照，可选专题与实际能力分开验收。",
        "",
        "学习目标：完成本等级的每课操作与验收，产出可观察的验证结果。",
        "",
    ]
    for index, (topic, goal, exercise, acceptance) in enumerate(COURSE_LESSONS[level], 1):
        lines.extend(
            [
                f"第 {index} {'天' if plan else '课'}：{topic}",
                f"- 目标：{goal}",
                f"- 练习：{exercise}",
                f"- 验收：{acceptance}",
                "",
            ]
        )
    lines.append(
        "仓库示例需源码工作区；安装包通过内置 Resource/Tool 获取内容，不读取仓库相对路径。"
    )
    return "\n".join(lines)


CURRICULUMS = {level: _course(level) for level in LEARNING_LEVELS}
LEARNING_PLANS = {level: _course(level, plan=True) for level in LEARNING_LEVELS}

__all__ = [
    "COURSE_LESSONS",
    "CURRICULUMS",
    "LEARNING_LEVELS",
    "LEARNING_PLANS",
    "LEARNING_SEQUENCE",
]
