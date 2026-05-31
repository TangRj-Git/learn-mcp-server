from learn_mcp_server.data.curriculum import CURRICULUMS
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def get_curriculum_beginner() -> str:
    return CURRICULUMS["beginner"].strip()


def get_curriculum_intermediate() -> str:
    return CURRICULUMS["intermediate"].strip()


def get_curriculum_advanced() -> str:
    return CURRICULUMS["advanced"].strip()


def get_curriculum_resource(level: str) -> str:
    normalized_level = normalize_key(require_not_blank(level, "level"))

    if normalized_level not in CURRICULUMS:
        available_levels = format_available_items(list(CURRICULUMS.keys()))
        return f"没有找到课程：{level}\n\n当前支持的课程包括：\n\n{available_levels}"

    return CURRICULUMS[normalized_level].strip()


__all__ = [
    "get_curriculum_advanced",
    "get_curriculum_beginner",
    "get_curriculum_intermediate",
    "get_curriculum_resource",
]
