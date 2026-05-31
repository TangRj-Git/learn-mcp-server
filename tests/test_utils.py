import pytest

from learn_mcp_server.utils import (
    format_available_items,
    format_markdown_list,
    normalize_key,
    require_not_blank,
    require_string_list,
)


def test_normalize_key_trims_and_lowercases_value():
    assert normalize_key("  Tool  ") == "tool"


def test_require_not_blank_returns_trimmed_value():
    assert require_not_blank("  concept  ", "concept") == "concept"


def test_require_not_blank_rejects_empty_value():
    with pytest.raises(ValueError, match="concept 不能为空"):
        require_not_blank("   ", "concept")


def test_format_available_items_joins_items():
    assert format_available_items(["tool", "resource", "prompt"]) == "tool, resource, prompt"


def test_format_markdown_list_formats_bullets():
    assert format_markdown_list(["tool", "resource"]) == "- tool\n- resource"


def test_require_string_list_returns_string_list():
    assert require_string_list(["server.py"], "args") == ["server.py"]


def test_require_string_list_rejects_non_list_value():
    with pytest.raises(ValueError, match="args 必须是字符串列表"):
        require_string_list("server.py", "args")


def test_require_string_list_rejects_non_string_items():
    with pytest.raises(ValueError, match="args 必须是字符串列表"):
        require_string_list(["server.py", 123], "args")
