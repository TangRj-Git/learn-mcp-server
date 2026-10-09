from typing import Literal

from learn_mcp_server.data.concepts import CONCEPTS
from learn_mcp_server.data.curriculum import LEARNING_LEVELS, LEARNING_PLANS, LEARNING_SEQUENCE
from learn_mcp_server.data.practices import PRACTICE_TASKS
from learn_mcp_server.utils import (
    format_available_items,
    normalize_key,
    require_choice,
    require_not_blank,
)


def generate_learning_plan(level: Literal["beginner", "intermediate", "advanced"]) -> str:
    """返回对应等级的目标、练习和验收；未知等级不静默替换。"""
    return LEARNING_PLANS[require_choice(level, "level", LEARNING_LEVELS)]


def get_practice_task(topic: str) -> str:
    """读取某个主题的练习和专属验收标准，不执行代码。"""
    key = normalize_key(require_not_blank(topic, "topic"))
    if key not in PRACTICE_TASKS:
        return f"没有找到练习主题：{topic}\n\n当前支持的练习主题包括：\n\n{format_available_items(list(PRACTICE_TASKS))}"
    practice = PRACTICE_TASKS[key]
    checks = "\n".join(f"{index}. {check}" for index, check in enumerate(practice["checks"], 1))
    return f"# {practice['title']}\n\n任务：\n\n{practice['task']}\n\n完成标准：\n\n{checks}\n\n关键词自查不能代替实际运行和语义审阅。"


def check_answer(topic: str, answer: str) -> str:
    """关键词辅助自查：列出覆盖与遗漏，不能判断回答是否正确。"""
    key = normalize_key(require_not_blank(topic, "topic"))
    normalized_answer = normalize_key(require_not_blank(answer, "answer"))
    practice = PRACTICE_TASKS.get(key)
    if practice is None:
        return f"暂时不能检查主题：{topic}\n\n当前支持的主题包括：\n\n{format_available_items(list(PRACTICE_TASKS))}"
    lines = [
        "# 答案反馈：关键词辅助自查",
        "",
        f"主题：{practice['title']}",
        "",
        "这不是语义判卷。命中关键词不能证明观点正确，否定或错误表述也可能命中。",
        "",
    ]
    for label, keywords in practice["checkpoints"].items():
        matched = [keyword for keyword in keywords if keyword.lower() in normalized_answer]
        lines.append(
            f"- {label}："
            + (
                f"检测到关键词 {', '.join(matched)}；请核对实际含义。"
                if matched
                else f"尚未检测到；可参考 {', '.join(keywords)}。"
            )
        )
    lines.extend(
        [
            "",
            "下一步：按 get_practice_task 的验收标准运行 Client；需要语义点评时使用 Host 模型审阅，不在 Server 内调用外部模型。",
        ]
    )
    return "\n".join(lines)


def suggest_next_step(current_topic: str) -> str:
    """沿有效主题序列推荐下一步；完成节点不会返回起点。"""
    key = normalize_key(require_not_blank(current_topic, "current_topic"))
    if key not in CONCEPTS:
        return (
            f"没有找到主题：{current_topic}\n\n可用主题：{format_available_items(list(CONCEPTS))}"
        )
    if key not in LEARNING_SEQUENCE or key == LEARNING_SEQUENCE[-1]:
        return f"# 下一步学习建议\n\n当前主题：{key}\n\n这一阶段已完成。用完整 Client 综合验证 Tool、Resource、Prompt，再选择 mcp://curriculum/advanced 复习版本与边界。"
    next_topic = LEARNING_SEQUENCE[LEARNING_SEQUENCE.index(key) + 1]
    return f"""# 下一步学习建议

当前主题：{key}

推荐下一步：{next_topic}

建议操作：
1. 调用 explain_concept("{next_topic}")，或读取 mcp://concepts/{next_topic}。
2. 根据课程查看示例和练习；完成验收后继续。
3. Resource/Prompt、schema、错误与真实传输均应实际观察。

后续衔接：{" -> ".join(LEARNING_SEQUENCE)}
"""


__all__ = ["check_answer", "generate_learning_plan", "get_practice_task", "suggest_next_step"]
