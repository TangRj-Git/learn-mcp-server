from learn_mcp_server.data.concepts import CONCEPTS
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

{CONCEPTS[normalized_concept].strip()}
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

    return f"""
# {left_key} 和 {right_key} 的对比

## {left_key}

{CONCEPTS[left_key].strip()}

---

## {right_key}

{CONCEPTS[right_key].strip()}

---

## 简单总结

{left_key} 和 {right_key} 都是 MCP 学习中的重要概念。

如果一个概念偏向“执行动作”，通常更接近 Tool。
如果一个概念偏向“提供上下文内容”，通常更接近 Resource。
如果一个概念偏向“复用任务模板”，通常更接近 Prompt。
如果一个概念偏向“连接和管理”，通常更接近 Host、Client、Server 这一层。
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
- Resource：模型可读取的上下文，适合文档、资料、配置、示例。
- Prompt：可复用的提示词模板，适合固定任务流程和教学引导。

## 通信关系

Client 和 Server 之间通过 Transport 传输 JSON-RPC 消息。
本地常用 stdio，长期运行或远程访问常用 streamable-http。

## 学习顺序

MCP -> Host/Client/Server -> Tool -> Resource -> Resource Template -> Prompt -> Transport -> 配置与调试
""".strip()


__all__ = ["compare_concepts", "explain_concept", "get_concept_map"]
