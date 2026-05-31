CODE_EXAMPLES = {
    "basic-tool": """
# basic-tool

下面是一个最小 MCP Tool 示例：

```python
@mcp.tool()
def get_server_info() -> str:
    return "learn-mcp-server"
```

这个示例说明：普通 Python 函数可以通过 @mcp.tool() 注册成模型可调用的 Tool。
""",
    "basic-resource": """
# basic-resource

下面是一个最小 MCP Resource 示例：

```python
@mcp.resource("mcp://docs/introduction")
def get_docs_introduction() -> str:
    return "MCP 入门文档"
```

这个示例说明：Resource 通过 URI 暴露可读取的上下文内容。
""",
    "resource-template": """
# resource-template

下面是一个最小 MCP Resource Template 示例：

```python
@mcp.resource("mcp://concepts/{name}")
def get_concept_resource(name: str) -> str:
    return f"概念名称：{name}"
```

这个示例说明：URI 中的 {name} 会映射到同名函数参数 name。
""",
    "basic-prompt": """
# basic-prompt

下面是一个最小 MCP Prompt 示例：

```python
@mcp.prompt()
def explain_mcp_topic(topic: str, level: str) -> str:
    return f"请用 {level} 水平解释 MCP 主题：{topic}"
```

这个示例说明：Prompt 适合封装可复用的任务提示词模板。
""",
    "tool-params": """
# tool-params

下面是一个带参数的 MCP Tool 示例：

```python
@mcp.tool()
def explain_concept(concept: str) -> str:
    return f"解释概念：{concept}"
```

这个示例说明：函数参数会成为 Tool 的输入 schema。
""",
    "async-tool": """
# async-tool

下面是一个异步 MCP Tool 示例：

```python
@mcp.tool()
async def fetch_status(url: str) -> str:
    return "ok"
```

这个示例说明：FastMCP 可以注册 async 函数。
""",
    "error-handling": """
# error-handling

下面是一个错误处理示例：

```python
@mcp.tool()
def explain_concept(concept: str) -> str:
    if not concept.strip():
        raise ValueError("concept 不能为空")
    return concept
```

这个示例说明：Tool 可以通过清晰的异常信息帮助调用方理解输入错误。
""",
    "end-to-end-client": """
# end-to-end-client

下面是一个端到端 FastMCP Client 示例，它会列出能力、调用 Tool、读取 Resource，并获取 Prompt：

```python
import asyncio

from fastmcp import Client
from learn_mcp_server.server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        tool_result = await client.call_tool("explain_concept", {"concept": "tool"})
        resource_result = await client.read_resource("mcp://docs/introduction")
        prompt_result = await client.get_prompt(
            "explain_mcp_topic",
            {"topic": "resource", "level": "beginner"},
        )

    print([tool.name for tool in tools])
    print([resource.uri for resource in resources])
    print([prompt.name for prompt in prompts])
    print(tool_result.data)
    print(resource_result[0].text)
    print(prompt_result.messages[0].content.text)


asyncio.run(main())
```

这个示例说明：学习 MCP 时，不只要知道 Tool、Resource、Prompt 怎么写，还要知道 Client 如何发现并使用它们。
""",
}

__all__ = ["CODE_EXAMPLES"]
