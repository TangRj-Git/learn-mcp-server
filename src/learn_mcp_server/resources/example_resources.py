from learn_mcp_server.data.examples import CODE_EXAMPLES
from learn_mcp_server.utils import format_available_items, normalize_key, require_not_blank


def get_example_basic_tool() -> str:
    return CODE_EXAMPLES["basic-tool"].strip()


def get_example_basic_resource() -> str:
    return CODE_EXAMPLES["basic-resource"].strip()


def get_example_resource_template() -> str:
    return CODE_EXAMPLES["resource-template"].strip()


def get_example_basic_prompt() -> str:
    return CODE_EXAMPLES["basic-prompt"].strip()


def get_example_tool_basic() -> str:
    return CODE_EXAMPLES["basic-tool"].strip()


def get_example_resource_basic() -> str:
    return CODE_EXAMPLES["basic-resource"].strip()


def get_example_prompt_basic() -> str:
    return CODE_EXAMPLES["basic-prompt"].strip()


def get_example_tool_params() -> str:
    return CODE_EXAMPLES["tool-params"].strip()


def get_example_async_tool() -> str:
    return CODE_EXAMPLES["async-tool"].strip()


def get_example_error_handling() -> str:
    return CODE_EXAMPLES["error-handling"].strip()


def get_example_end_to_end_client() -> str:
    return CODE_EXAMPLES["end-to-end-client"].strip()


def get_example_resource(name: str) -> str:
    normalized_name = normalize_key(require_not_blank(name, "name"))

    if normalized_name not in CODE_EXAMPLES:
        available_examples = format_available_items(list(CODE_EXAMPLES.keys()))
        return f"没有找到示例：{name}\n\n当前支持的示例包括：\n\n{available_examples}"

    return CODE_EXAMPLES[normalized_name].strip()


__all__ = [
    "get_example_async_tool",
    "get_example_basic_prompt",
    "get_example_basic_resource",
    "get_example_basic_tool",
    "get_example_end_to_end_client",
    "get_example_error_handling",
    "get_example_prompt_basic",
    "get_example_resource",
    "get_example_resource_basic",
    "get_example_resource_template",
    "get_example_tool_basic",
    "get_example_tool_params",
]
