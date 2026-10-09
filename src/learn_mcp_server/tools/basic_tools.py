from importlib.metadata import version

from learn_mcp_server import __version__
from learn_mcp_server.data.concepts import LEARNING_MODULES
from learn_mcp_server.data.curriculum import LEARNING_SEQUENCE
from learn_mcp_server.data.references import BASELINE
from learn_mcp_server.settings import PROJECT_NAME
from learn_mcp_server.utils import format_markdown_list


def get_server_info() -> str:
    """获取项目版本、运行依赖、协议基线与学习能力。"""
    return f"""# {PROJECT_NAME}

这是一个用于学习 MCP 的 FastMCP Server。

项目版本：{__version__}；FastMCP：{version("fastmcp")}；SDK：{version("mcp")}。
教学基线：{BASELINE}。默认 Client 自动协商 modern；旧握手仅作历史对照，可选专题不等于已实现。

1. get_server_info / list_learning_modules / get_learning_path：信息与路线
2. explain_concept / compare_concepts / get_concept_map：概念、比较与出处
3. 示例、专属练习、配置静态校验与调试诊断
4. Markdown Resources、Resource Templates 和 Prompt 消息模板

check_answer 只作关键词自查；Prompt 获取不自动调用模型。
工具不执行提交的代码或命令，不读取用户文件，不探测网络。
"""


def list_learning_modules() -> str:
    """列出主课程、历史专题与最新规范对照模块。"""
    lines = ["# MCP 学习模块", "", BASELINE, ""]
    for index, module in enumerate(LEARNING_MODULES, 1):
        lines.extend([f"## {index}. {module['name']}", "", module["description"], "", "包含主题："])
        lines.extend(format_markdown_list(module["topics"]).splitlines())
        lines.append("")
    return "\n".join(lines)


def get_learning_path() -> str:
    """返回有效主题的学习路线，最后进入综合验证。"""
    steps = "\n\n".join(
        f"第 {index} 步：{topic}，读取 mcp://concepts/{topic}。"
        for index, topic in enumerate(LEARNING_SEQUENCE, 1)
    )
    return f"# MCP 学习路径\n\n{BASELINE}\n\n{steps}\n\nTool -> Resource -> Prompt 后学习 schema、错误与真实传输，最后完成综合验证。"


__all__ = ["get_learning_path", "get_server_info", "list_learning_modules"]
