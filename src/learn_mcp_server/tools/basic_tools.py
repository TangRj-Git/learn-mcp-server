from learn_mcp_server.data.concepts import LEARNING_MODULES
from learn_mcp_server.settings import PROJECT_NAME
from learn_mcp_server.utils import format_markdown_list


def get_server_info() -> str:
    """
    获取这个学习 MCP Server 的基本信息。
    """
    return f"""
# {PROJECT_NAME}

这是一个用于学习 MCP 的 FastMCP Server。

当前版本包含：

1. get_server_info：查看 Server 基本信息
2. list_learning_modules：查看学习模块
3. get_learning_path：查看推荐学习路径
4. explain_concept / get_concept_map：解释 MCP 概念和关系图
5. MCP 示例、练习、配置生成、安全边界和调试诊断工具
6. MCP Resources、Resource Templates 和 Prompts
"""


def list_learning_modules() -> str:
    """
    列出当前学习 MCP Server 支持的学习模块。
    """
    lines = ["# MCP 学习模块", ""]

    for index, module in enumerate(LEARNING_MODULES, start=1):
        lines.append(f"## {index}. {module['name']}")
        lines.append("")
        lines.append(module["description"])
        lines.append("")
        lines.append("包含主题：")
        lines.extend(format_markdown_list(module["topics"]).splitlines())
        lines.append("")

    return "\n".join(lines)


def get_learning_path() -> str:
    """
    返回一个适合初学者按顺序学习 MCP 的路线图。
    """
    return """
# MCP 学习路径

第 1 步：理解 MCP、Host、Client、Server 的关系。

第 2 步：学习 Tool，知道模型什么时候应该调用一个可执行动作。

第 3 步：学习 Resource，理解可读取上下文和可执行动作的区别。

第 4 步：学习 Resource Template，掌握带参数 URI 的动态资源。

第 5 步：学习 Prompt，封装可复用的任务提示词模板。

第 6 步：理解 stdio 和 streamable-http 两种传输方式。

第 7 步：学习 Host 配置、Inspector 调试和常见错误排查。

第 8 步：学习 elicitation、authorization、security 和长时间运行任务的设计边界。

第 9 步：用测试和客户端脚本验证 Tools、Resources、Resource Templates、Prompts 是否真的可用。
""".strip()


__all__ = ["get_learning_path", "get_server_info", "list_learning_modules"]
