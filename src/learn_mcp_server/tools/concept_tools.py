"""概念查询与对比，正文和官方依据来自 data。"""

from learn_mcp_server.data.concepts import CONCEPT_COMPARISONS, CONCEPTS
from learn_mcp_server.data.references import reference_note
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def explain_concept(concept: str) -> str:
    """
    根据概念名称解释 MCP 相关概念。
    """
    normalized_concept = normalize_key(require_not_blank(concept, "concept"))

    if normalized_concept not in CONCEPTS:
        available_concepts = format_available_items(list(CONCEPTS.keys()))
        return f"没有找到概念：{concept}\n\n当前支持的概念包括：\n\n{available_concepts}"

    return f"""
# {normalized_concept}

{CONCEPTS[normalized_concept].strip()}{reference_note(normalized_concept)}
"""


def compare_concepts(left: str, right: str) -> str:
    """
    对比两个 MCP 概念的区别。
    """
    left_key = normalize_key(require_not_blank(left, "left"))
    right_key = normalize_key(require_not_blank(right, "right"))

    if left_key not in CONCEPTS:
        available_concepts = format_available_items(list(CONCEPTS.keys()))
        return f"没有找到概念：{left}\n\n当前支持的概念包括：\n\n{available_concepts}"

    if right_key not in CONCEPTS:
        available_concepts = format_available_items(list(CONCEPTS.keys()))
        return f"没有找到概念：{right}\n\n当前支持的概念包括：\n\n{available_concepts}"

    pair = (left_key, right_key)
    rows = CONCEPT_COMPARISONS.get(pair)
    if rows is None and (right_key, left_key) in CONCEPT_COMPARISONS:
        rows = [
            (label, right_value, left_value)
            for label, left_value, right_value in CONCEPT_COMPARISONS[(right_key, left_key)]
        ]
    comparison = (
        "\n".join(
            [
                f"| 维度 | {left_key} | {right_key} |",
                "| --- | --- | --- |",
                *(
                    f"| {label} | {left_value} | {right_value} |"
                    for label, left_value, right_value in rows
                ),
            ]
        )
        if rows
        else "此组合没有专门比较表，以下提供定义与官方出处；请结合实际使用场景判断。"
    )

    return f"""
# {left_key} 和 {right_key} 的对比

{comparison}

## {left_key}

{CONCEPTS[left_key].strip()}{reference_note(left_key)}

---

## {right_key}

{CONCEPTS[right_key].strip()}{reference_note(right_key)}
"""


def get_concept_map() -> str:
    """
    返回 MCP 核心概念之间的关系图谱。
    """
    return """
# MCP 概念地图

## 架构关系

Host 是用户真正使用的应用。
Client 通常存在于 Host 内部，负责和 MCP Server 通信。
Server 提供 MCP 能力，供 Host 通过 Client 发现和使用。

## 能力关系

Server 可以暴露三类核心能力：

- Tool：模型可调用的动作，适合执行、查询、生成、处理。
- Resource：应用选择加入上下文的资料（application-controlled）。
- Prompt：用户选择的消息模板（user-controlled），获取不自动调用模型。

## 通信关系

Client 和 Server 之间通过 Transport 传输 JSON-RPC 消息。
本地常用 stdio，长期运行或远程访问常用 streamable-http。

## 学习顺序

MCP -> Host/Client/Server -> Tool -> Resource -> Resource Template -> Prompt -> Transport -> 配置与调试
""".strip()


__all__ = ["compare_concepts", "explain_concept", "get_concept_map"]
