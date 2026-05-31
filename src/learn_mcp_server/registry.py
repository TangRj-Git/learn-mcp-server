from collections.abc import Callable
from typing import Any

from fastmcp import FastMCP

from learn_mcp_server.prompts import learning_prompts
from learn_mcp_server.resources import (
    concept_resources,
    config_resources,
    curriculum_resources,
    debug_resources,
    example_resources,
)
from learn_mcp_server.tools import (
    basic_tools,
    concept_tools,
    config_tools,
    debug_tools,
    example_tools,
    practice_tools,
)

RegisteredFunctions = dict[str, Callable[..., Any]]

TOOLS: tuple[tuple[str, Callable[..., Any]], ...] = (
    ("get_server_info", basic_tools.get_server_info),
    ("list_learning_modules", basic_tools.list_learning_modules),
    ("get_learning_path", basic_tools.get_learning_path),
    ("explain_concept", concept_tools.explain_concept),
    ("compare_concepts", concept_tools.compare_concepts),
    ("get_concept_map", concept_tools.get_concept_map),
    ("list_code_examples", example_tools.list_code_examples),
    ("get_code_example", example_tools.get_code_example),
    ("explain_code_example", example_tools.explain_code_example),
    ("generate_learning_plan", practice_tools.generate_learning_plan),
    ("get_practice_task", practice_tools.get_practice_task),
    ("check_answer", practice_tools.check_answer),
    ("suggest_next_step", practice_tools.suggest_next_step),
    ("explain_config", config_tools.explain_config),
    ("generate_stdio_config", config_tools.generate_stdio_config),
    ("generate_http_config", config_tools.generate_http_config),
    ("compare_local_and_remote_config", config_tools.compare_local_and_remote_config),
    ("diagnose_issue", debug_tools.diagnose_issue),
    ("explain_error_message", debug_tools.explain_error_message),
    ("list_common_errors", debug_tools.list_common_errors),
)

RESOURCES: tuple[tuple[str, str, Callable[..., Any]], ...] = (
    ("get_docs_introduction", "mcp://docs/introduction", concept_resources.get_docs_introduction),
    ("get_docs_tools", "mcp://docs/tools", concept_resources.get_docs_tools),
    ("get_docs_resources", "mcp://docs/resources", concept_resources.get_docs_resources),
    ("get_docs_prompts", "mcp://docs/prompts", concept_resources.get_docs_prompts),
    ("get_docs_transports", "mcp://docs/transports", concept_resources.get_docs_transports),
    ("get_docs_architecture", "mcp://docs/architecture", concept_resources.get_docs_architecture),
    ("get_docs_host_client_server", "mcp://docs/host-client-server", concept_resources.get_docs_host_client_server),
    ("get_docs_concepts", "mcp://docs/concepts", concept_resources.get_docs_concepts),
    ("get_docs_resource_template", "mcp://docs/resource-template", concept_resources.get_docs_resource_template),
    ("get_docs_stdio", "mcp://docs/stdio", concept_resources.get_docs_stdio),
    ("get_docs_streamable_http", "mcp://docs/streamable-http", concept_resources.get_docs_streamable_http),
    ("get_docs_json_rpc", "mcp://docs/json-rpc", concept_resources.get_docs_json_rpc),
    ("get_docs_lifecycle", "mcp://docs/lifecycle", concept_resources.get_docs_lifecycle),
    ("get_docs_elicitation", "mcp://docs/elicitation", concept_resources.get_docs_elicitation),
    ("get_docs_authorization", "mcp://docs/authorization", concept_resources.get_docs_authorization),
    ("get_docs_security", "mcp://docs/security", concept_resources.get_docs_security),
    ("get_docs_tasks", "mcp://docs/tasks", concept_resources.get_docs_tasks),
    ("get_curriculum_beginner", "mcp://curriculum/beginner", curriculum_resources.get_curriculum_beginner),
    (
        "get_curriculum_intermediate",
        "mcp://curriculum/intermediate",
        curriculum_resources.get_curriculum_intermediate,
    ),
    ("get_curriculum_advanced", "mcp://curriculum/advanced", curriculum_resources.get_curriculum_advanced),
    ("get_example_basic_tool", "mcp://examples/basic-tool", example_resources.get_example_basic_tool),
    ("get_example_basic_resource", "mcp://examples/basic-resource", example_resources.get_example_basic_resource),
    ("get_example_tool_basic", "mcp://examples/tool-basic", example_resources.get_example_tool_basic),
    ("get_example_resource_basic", "mcp://examples/resource-basic", example_resources.get_example_resource_basic),
    (
        "get_example_resource_template",
        "mcp://examples/resource-template",
        example_resources.get_example_resource_template,
    ),
    ("get_example_basic_prompt", "mcp://examples/basic-prompt", example_resources.get_example_basic_prompt),
    ("get_example_prompt_basic", "mcp://examples/prompt-basic", example_resources.get_example_prompt_basic),
    ("get_example_tool_params", "mcp://examples/tool-params", example_resources.get_example_tool_params),
    ("get_example_async_tool", "mcp://examples/async-tool", example_resources.get_example_async_tool),
    ("get_example_error_handling", "mcp://examples/error-handling", example_resources.get_example_error_handling),
    ("get_example_end_to_end_client", "mcp://examples/end-to-end-client", example_resources.get_example_end_to_end_client),
    ("get_debug_common_errors", "mcp://debug/common-errors", debug_resources.get_debug_common_errors),
    ("get_debug_stdio_errors", "mcp://debug/stdio-errors", debug_resources.get_debug_stdio_errors),
    ("get_debug_http_errors", "mcp://debug/http-errors", debug_resources.get_debug_http_errors),
    ("get_debug_config_errors", "mcp://debug/config-errors", debug_resources.get_debug_config_errors),
    ("get_docs_config_stdio", "mcp://docs/config-stdio", config_resources.get_docs_config_stdio),
    ("get_docs_config_http", "mcp://docs/config-http", config_resources.get_docs_config_http),
    (
        "get_docs_config_local_vs_remote",
        "mcp://docs/config-local-vs-remote",
        config_resources.get_docs_config_local_vs_remote,
    ),
    ("get_docs_config_common_errors", "mcp://docs/config-common-errors", config_resources.get_docs_config_common_errors),
)

RESOURCE_TEMPLATES: tuple[tuple[str, str, Callable[..., Any]], ...] = (
    ("get_concept_resource", "mcp://concepts/{name}", concept_resources.get_concept_resource),
    ("get_example_resource", "mcp://examples/{name}", example_resources.get_example_resource),
    ("get_debug_resource", "mcp://debug/{error_type}", debug_resources.get_debug_resource),
    ("get_config_resource", "mcp://configs/{name}", config_resources.get_config_resource),
    ("get_curriculum_resource", "mcp://curriculum/{level}", curriculum_resources.get_curriculum_resource),
)

PROMPTS: tuple[tuple[str, Callable[..., Any]], ...] = (
    ("explain_mcp_topic", learning_prompts.explain_mcp_topic),
    ("generate_mcp_study_plan", learning_prompts.generate_mcp_study_plan),
    ("review_mcp_code", learning_prompts.review_mcp_code),
    ("debug_mcp_error", learning_prompts.debug_mcp_error),
    ("summarize_mcp_concept", learning_prompts.summarize_mcp_concept),
)


def register_tools(mcp: FastMCP) -> RegisteredFunctions:
    return {name: mcp.tool()(function) for name, function in TOOLS}


def register_resources(mcp: FastMCP) -> RegisteredFunctions:
    registered: RegisteredFunctions = {}
    for name, uri, function in (*RESOURCES, *RESOURCE_TEMPLATES):
        registered[name] = mcp.resource(uri)(function)
    return registered


def register_prompts(mcp: FastMCP) -> RegisteredFunctions:
    return {name: mcp.prompt()(function) for name, function in PROMPTS}


def register_all(mcp: FastMCP) -> RegisteredFunctions:
    registered: RegisteredFunctions = {}
    registered.update(register_tools(mcp))
    registered.update(register_resources(mcp))
    registered.update(register_prompts(mcp))
    return registered


__all__ = [
    "PROMPTS",
    "REGISTERED_NAMES",
    "RESOURCES",
    "RESOURCE_TEMPLATES",
    "TOOLS",
    "register_all",
    "register_prompts",
    "register_resources",
    "register_tools",
]

REGISTERED_NAMES = tuple(
    name for name, _ in (*TOOLS, *PROMPTS)
) + tuple(name for name, _, _ in (*RESOURCES, *RESOURCE_TEMPLATES))
