"""可独立运行的学习示例；由包内源码同时提供可执行示例和展示文本。"""

import json
import math
from typing import Annotated, Literal

from fastmcp import FastMCP
from fastmcp.dependencies import CurrentContext
from fastmcp.exceptions import ResourceError, ToolError
from fastmcp.prompts import Message
from fastmcp.server.context import Context
from pydantic import Field

mcp = FastMCP(
    "learning-demo",
    version="0.1.0",
    instructions="FastMCP 4.x / SDK 2.x / 协议 2026-07-28 的三原语示例，不调用模型。",
)
TOPICS = {
    "tool": "Tool：模型提出调用的动作；调用与授权分开。",
    "resource": "Resource：由应用选择使用的上下文，list 元数据与 read 正文不同。",
    "prompt": "Prompt：用户选择的消息模板，获取不自动调用模型。",
}


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": False})
def divide(
    a: Annotated[float, Field(description="被除数", allow_inf_nan=False)],
    b: Annotated[float, Field(description="非零除数", allow_inf_nan=False)],
    mode: Literal["exact", "rounded"] = "exact",
) -> dict[str, float]:
    """两数相除，返回符合 outputSchema 的对象。"""
    if not math.isfinite(a) or not math.isfinite(b):
        raise ToolError("输入必须是有限数值。")
    if b == 0:
        raise ToolError("b 不能为零。")
    if mode not in {"exact", "rounded"}:
        raise ToolError("mode 只能是 exact 或 rounded。")
    value = a / b
    if not math.isfinite(value):
        raise ToolError("结果超出有限数值范围。")
    return {"value": value if mode == "exact" else round(value, 2)}


@mcp.resource("demo://metadata", mime_type="application/json")
def demo_metadata() -> str:
    """读取 JSON 元数据；显式序列化，并观察实际 MIME。"""
    return json.dumps(
        {"version": "0.1.0", "protocol": "2026-07-28", "topics": list(TOPICS)}, ensure_ascii=False
    )


@mcp.resource("demo://topics/{name}{?detail}", mime_type="text/markdown")
def topic_document(name: str, detail: bool = False) -> str:
    """读取带路径参数与可选查询参数的 Markdown；未知名称明确失败。"""
    name = name.strip().lower()
    if name not in TOPICS:
        raise ResourceError("未知主题，可用：tool、resource、prompt。")
    text = f"# {name}\n\n{TOPICS[name]}"
    if detail:
        text += "\n\n验收：通过 Client 观察发现、输入、结果和失败行为。"
    return text


@mcp.prompt()
def explain_topic(topic: str) -> list[Message]:
    """返回 user/assistant 消息；Client 获取模板后自行决定怎样使用。"""
    if not topic.strip():
        raise ValueError("topic 不能为空。")
    return [
        Message(f"请解释 MCP 主题 {topic}，先给定义，再给一个可观察的例子。"),
        Message("我会区分协议、框架和客户端行为。", role="assistant"),
    ]


@mcp.prompt()
def study_plan(
    days: Annotated[int, Field(ge=1, le=30)] = 7,
    level: Literal["beginner", "intermediate", "advanced"] = "beginner",
) -> str:
    """返回计划请求；协议 arguments 中 days 传字符串，如 '3'。"""
    if isinstance(days, bool) or not isinstance(days, int) or not 1 <= days <= 30:
        raise ValueError("days 必须是 1–30 的整数。")
    goals = {
        "beginner": "运行三原语",
        "intermediate": "检查 schema、错误和传输",
        "advanced": "对照新旧协议与安全边界",
    }
    if level not in goals:
        raise ValueError("未知 level。")
    return f"请给出 {days} 天计划，目标：{goals[level]}。每天有操作与验收；基线 FastMCP 4.x。"


@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": False})
async def count_steps(ctx: Context = CurrentContext()) -> dict[str, int]:
    """报告三个确定步骤；Context 不作为模型输入参数，不访问外部数据。"""
    for step in range(1, 4):
        await ctx.report_progress(progress=step, total=3)
    return {"steps": 3}


def main() -> None:
    """启动 stdio；导入本模块不会启动服务。"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
