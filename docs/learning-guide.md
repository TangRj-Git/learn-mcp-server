# MCP 学习指南：运行、观察与验收

主课程基线：FastMCP 4.1.0 / MCP Python SDK 2.3.0 / MCP 2026-07-28。安装与连接步骤见 [运行与配置](running-and-configuration.md)，新旧协议与迁移见 [版本说明](protocol-versions.md)。以下 Python Client 代码在已安装本项目的环境运行。

主服务提供教材与自查；独立示例 `learn_mcp_server.demo` 展示具体协议行为。读取 `mcp://...` 的资料使用主服务；调用 `divide`、读取 `demo://...` 使用独立示例。两份实例不会自动合并。

## 入门：先得到可观察的结果

### 1. 发现能力

先运行：

```powershell
uv sync --locked
uv run --locked python examples/client_test.py
uv run --locked python examples/client_test.py --demo
```

这两个脚本用内存连接，不启动子进程。主服务预期 20 Tools / 39 Resources / 5 Templates / 5 Prompts；教学示例预期 2 Tools / 1 Resource / 1 Template / 2 Prompts。

下面是可独立保存运行的 Client。它复用包内教学实例；导入不会启动 stdio：

```python
import asyncio

from fastmcp import Client
from learn_mcp_server.demo import mcp


async def main():
    async with Client(mcp, timeout=10) as client:
        tools = await client.list_tools()
        templates = await client.list_resource_templates()
        result = await client.call_tool("divide", {"a": 6, "b": 2})
        document = await client.read_resource("demo://topics/tool?detail=true")
        prompt = await client.get_prompt("explain_topic", {"topic": "tool"})
    print([tool.name for tool in tools])
    print([template.uri_template for template in templates])
    print(result.structured_content)
    print(document[0].mime_type, document[0].text)
    print([message.role for message in prompt.messages])


asyncio.run(main())
```

验收：看到 `divide` 与 `count_steps`；`structured_content` 为 `{"value": 3.0}`；Template 实际内容是 Markdown；Prompt 有 `user`、`assistant` 两条消息。

### 2. 区分三个原语

| 原语 | 典型控制方式 | 发现/使用 | 本例 |
| --- | --- | --- | --- |
| Tool | 模型提出调用；Host 处理确认与授权 | `tools/list` / `tools/call` | `divide` 执行计算 |
| Resource | 应用选择上下文 | `resources/list` / `resources/read` | `demo://metadata` 提供正文 |
| Prompt | 用户选择消息模板 | `prompts/list` / `prompts/get` | `explain_topic` 返回消息 |

Resource 不会自动进入模型上下文，Prompt 不会自动调用模型，模型提出 Tool 调用也不等于操作已获授权。

### 3. 写最小 Server

完整源码见 [demo.py](../src/learn_mcp_server/demo.py)。工作区入口 [minimal_server.py](../examples/minimal_server.py) 只负责导入和启动，完整源码随安装包提供：

```powershell
uv run --locked python examples/minimal_server.py
```

也可以调用主服务的 `get_code_example`，参数 `{"topic": "minimal-server"}`，把返回的 Python 代码块保存为文件运行。`schema`、`resource-query` 等主题是提取出的函数片段；所需 import、FastMCP 实例和入口在完整源码中。

验收：文件导入不启动服务，直接运行使用 stdio；用 Inspector 的 `demo.py:mcp` 或内存 Client 发现三原语。stdio 服务在等待协议输入时没有普通输出是正常状态。

### 4. 使用主服务的学习路线

主服务可读取：

```text
mcp://docs/introduction
mcp://docs/host-client-server
mcp://curriculum/beginner
mcp://curriculum/intermediate
mcp://curriculum/advanced
```

主服务调用示例：

| 工具 | 参数 | 应观察的内容 |
| --- | --- | --- |
| `explain_concept` | `{"concept":"tool"}` | 正文、适用版本、官方出处 |
| `compare_concepts` | `{"left":"tool","right":"resource"}` | 同维度对照表 |
| `generate_learning_plan` | `{"level":"beginner"}` | 每课目标、操作与验收 |
| `get_practice_task` | `{"topic":"tool"}` | 主题专属操作与检查点 |
| `suggest_next_step` | `{"current_topic":"tests"}` | 学习终点与综合验证 |

三个等级分别侧重运行三原语、结果与传输、版本和边界。`check_answer` 是关键词检查点自查，即使所有关键词出现，也不能证明答案语义正确；应运行示例并人工对照验收。

## 中级：检查数据与失败行为

### 5. schema 与业务校验

观察 `divide` 的 `inputSchema`：

- `a`、`b` 是必需数字，带参数说明。
- `mode` 是 `exact` / `rounded` 枚举，默认 `exact`。
- `count_steps` 的 Context 注入参数 `ctx` 不在输入 schema 中。
- `divide` 的 `outputSchema` 是包含数值属性的对象。

```python
tools = {tool.name: tool for tool in await client.list_tools()}
print(tools["divide"].input_schema)
print(tools["divide"].output_schema)
```

上述片段放在前面的 `async with Client(mcp)` 中运行。验证合法输入 `{"a":1,"b":3,"mode":"rounded"}` 得到 `{"value":0.33}`；`mode="bad"` 得到输入校验错误；`b=0` 得到业务错误。

SDK 2 的 Python 属性使用 snake_case，wire JSON 仍使用 `inputSchema` / `outputSchema`。schema 不会表达全部业务约束。FastMCP 4 默认允许某些兼容类型转换，直接调用普通 Python 函数也不会自动经过 MCP 注册验证，所以关键业务条件仍在函数内检查。`days` 的 1–30 范围是本项目的教学约束。

### 6. 返回值有不同层次

| 层次 | 本例观察 | 含义 |
| --- | --- | --- |
| Python return | `{"value": 3.0}` | 函数返回的对象 |
| MCP `content` | 包含 JSON 文本的内容块 | 面向内容消费的结果 |
| MCP `structuredContent` | `{"value": 3.0}` | wire 中机器可读结果 |
| Tool `outputSchema` | 对象 schema | 描述结构化结果形状 |
| FastMCP `structured_content` / `data` | 可直接访问的字典 | Client 便利接口，不是新的 wire 字段 |

结构化 Tool 结果与大模型的结构化生成是不同能力。本项目主服务讲解工具仍返回易读文本，教学计算工具返回对象。

### 7. 错误状态与 Client 异常

```python
from fastmcp.exceptions import ToolError

# 这两个调用片段放在 Client 上下文中。
error = await client.call_tool("divide", {"a": 1, "b": 0}, raise_on_error=False)
print(error.is_error, error.content[0].text)

try:
    await client.call_tool("divide", {"a": 1, "b": 0})
except ToolError as error:
    print(type(error).__name__, str(error))
```

验收：前者返回错误状态和“b 不能为零”的内容；后者按 Client 默认策略抛 `ToolError`。不能只检查返回文本里有没有“error”。

区分 Python 异常、MCP 工具错误结果和 JSON-RPC `error`。本次实测 **FastMCP 4.1.0 将未知 Tool 也转为 `isError=True` 的工具结果**；不能仅凭规范分类断言该框架一定抛协议异常。未知 Resource、非法 Prompt 参数在当前 Client 中表现为 SDK `MCPError`，使用 `from mcp.shared.exceptions import MCPError`。现代 wire 的完成结果还有 `resultType="complete"`。

### 8. Resource 元数据、正文与 MIME

```python
resources = await client.list_resources()
metadata = (await client.read_resource("demo://metadata"))[0]
print(resources[0].mime_type)
print(metadata.mime_type, metadata.text)
```

列表返回元数据，读取返回 `contents`。`demo://metadata` 的正文能被 `json.loads()` 解析，读取 MIME 是 `application/json`。主服务教材是 `text/markdown`。

FastMCP 4.1.0 的 Template 声明 `mime_type="text/markdown"` 后直接返回 `str`，本次实际读取保留 `text/markdown`。因此主服务和完整示例都直接返回字符串，已移除 v3 阶段的 MIME 包装。验证实际读取结果，不只检查装饰器或列表。

### 9. Template 参数与 URI 边界

示例模式是 `demo://topics/{name}{?detail}`。必需参数 `name` 放在路径，可选查询参数 `detail` 有默认值 `False`，变量与函数参数对应。发现方法是 `resources/templates/list`，读取使用展开后的 URI。

| 实际 URI | 当前验证结果 |
| --- | --- |
| `demo://topics/tool` | Tool 基础正文 |
| `demo://topics/resource` | 不同主题的正文 |
| `demo://topics/tool?detail=true` | 增加验收说明 |
| `demo://topics/%74ool` | 百分号解码后匹配 `tool` |
| `demo://topics/unknown` | 明确报未知主题 |
| `demo://topics/tool%2Fresource` | 解码后不是支持的主题，报错 |
| `demo://topics/tool?detail=bad` | 非法布尔值报错 |

模式依据 RFC 6570，编码交给框架处理。URI 是资源标识，不是用户文件路径；`mcp://...`、`demo://...` 都不是 HTTP 服务地址。示例只支持三个固定主题，不将输入转换成文件路径。

主服务的未知概念/示例模板返回说明缺失及可用名称的帮助页，教学示例的未知主题抛明确错误；两种策略都不会把未知值静默替换为另一个主题。

### 10. Prompt 参数在线上是字符串

```python
prompt = await client.get_prompt("explain_topic", {"topic": "tool"})
print([message.role for message in prompt.messages])
plan = await client.get_prompt("study_plan", {"days": "3", "level": "advanced"})
print(plan.messages[0].content.text)
```

Prompt 协议的 arguments 是字符串，FastMCP 将 `"3"` 转换到函数的整数参数。有效输入得到消息，`"0"`、`"31"`、非法等级被拒绝。获取模板不会调用 LLM。

主服务的代码审查和错误分析 Prompt 将用户内容界定为待分析资料；这个文本约定不能替代 Host 对不可信内容的安全处理。

### 11. Context、进度、超时与取消

`count_steps` 通过 `CurrentContext()` 获取 FastMCP Context，并用 `report_progress` 报告三个步骤：

```python
events = []

async def on_progress(progress, total, message):
    events.append((progress, total))

result = await client.call_tool("count_steps", {}, progress_handler=on_progress)
print(events, result.structured_content)
```

验收：事件为 `(1,3)`、`(2,3)`、`(3,3)`，结果是 `{"steps":3}`。进度是与请求关联的通知；普通 async 和进度都不会自动变成后台 Task。

Client 示例设置有限超时并通过 `async with` 清理连接。`tests/test_client_lifecycle.py` 用无副作用的等待 Tool 验证超时和取消后，退出 Client 会执行函数的 `finally`；不能据此声称超时立即终止所有 Server 工作。SDK 2 超时表现为本地 `MCPError`，测试检查 `REQUEST_TIMEOUT`，不绑定错误文案；该 SDK 代码不是规范指定的对端错误码。

HTTP Client 退出不等于关闭独立 HTTP 服务。真实 stdio Client 管理子进程，测试使用 `keep_alive=False`。取消是合作行为，已经写入文件或提交的外部操作不会自动回滚；引入副作用后需单独考虑重试和幂等。

### 12. 真实传输与 JSON-RPC 观察

```powershell
uv run --locked python examples/transport_client.py stdio
```

HTTP 的两个终端步骤见 [运行与配置](running-and-configuration.md#http先启动服务再连接)。该脚本实际调用 Tool、读固定 Resource 和 Template、获取 Prompt。HTTP 测试另验证无/本地 Origin 成功、外部 Origin 为 403、外部 Host 为 421。

以下报文是 **2026-07-28 的教学示意**，用于解释字段，未声称是同一会话截取的连续日志。现代请求不先发 `initialize`，每次请求都携带协议版本与客户端能力。`server/discover` 对 Server 是必需方法，对 Client 是可选查询：

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "method": "server/discover",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {"name": "learning-client", "version": "1"}
    }
  }
}
```

完成响应有 `resultType`；身份在结果 `_meta` 中，具体工具 schema 仍查 `tools/list`：

```json
{
  "jsonrpc": "2.0",
  "id": "discover-1",
  "result": {
    "resultType": "complete",
    "supportedVersions": ["2026-07-28"],
    "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
    "_meta": {"io.modelcontextprotocol/serverInfo": {"name": "learning-demo", "version": "0.1.0"}},
    "ttlMs": 0,
    "cacheScope": "private"
  }
}
```

本次实际 `server/discover.supportedVersions` 只列 `2026-07-28`；旧协议兼容通过 legacy 初始化与调用另行验证，不能把这个清单当成所有历史协议的完整列表。使用 FastMCP Client 时，框架处理 metadata。若手工发送现代 HTTP 请求，还须镜像协议版本、method 与 name/uri，下面是调用教学示例的示意（本项目主 HTTP 入口未合并 demo）：

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: divide

{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "divide",
    "arguments": {"a": 6, "b": 2},
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {"name": "learning-client", "version": "1"}
    }
  }
}
```

`resources/read` 的 `Mcp-Name` 是 `params.uri`；`prompts/get` 是 `params.name`。不安全的非 ASCII header 值按规范的 Base64 sentinel 格式编码，本例名称均为 ASCII。headers 与正文不一致得到 HTTP 400 和 `HeaderMismatch`（-32020）。这里不能省略必需 headers。原始 HTTP 回归测试验证了这些约束，并证明无 initialize 时能发现和调用主服务。

成功响应的 `id` 与请求相同，Python Client 的 `structured_content` 对应 wire 的 `structuredContent`：

```json
{"jsonrpc":"2.0","id":10,"result":{"resultType":"complete","content":[{"type":"text","text":"{\"value\":3.0}"}],"structuredContent":{"value":3.0},"isError":false}}
```

协议错误响应只有 `error`，没有 `result`；工具业务错误可在完成结果中用 `isError` 表达：

```json
{"jsonrpc":"2.0","id":11,"error":{"code":-32601,"message":"Method not found"}}
```

```json
{"jsonrpc":"2.0","id":12,"result":{"resultType":"complete","content":[{"type":"text","text":"b 不能为零。"}],"isError":true}}
```

通知没有 `id`，不等待响应，进度示例已在第 11 课观察。`notifications/initialized` 仅属于旧握手，不能加入现代流程。discover/list/read 的完成结果要求缓存提示字段；`ttlMs=0` 表示立即过期，`cacheScope` 表示范围，并不提供身份授权。

Client 模式可直接对照：

```powershell
uv run --locked python examples/client_test.py --mode auto
uv run --locked python examples/client_test.py --mode 2026-07-28
uv run --locked python examples/client_test.py --mode legacy
```

前两个实测协议都是 2026-07-28，第三个是 2025-11-25。固定日期跳过发现，本版本实测 `server_info` 可为 `None`，脚本将 `server_version` 输出为 `null`；这不表示服务调用失败。若需要身份优先用 auto。`protocol_version` 等属性在退出 Client 后重置，应在 `async with` 内读取。没有 `mode="modern"` API。

在 Inspector 的请求/响应视图比较 method、id、metadata、arguments、result/error 和 `isError`；其具体协议支持取决于 Inspector 版本。不要往 stdio stdout 插入 `print`；普通诊断写 stderr。任意 JSON 文本都不等于合法 MCP 消息。

## 高级：版本、边界与可选能力

依次读取主服务 `mcp://concepts/latest-protocol`、`discovery`、`mrtr`、`subscriptions`、`caching`、`extensions`。当前已实测现代协议的发现、metadata、三原语、结果与缓存提示字段；MRTR 等交互仍需独立实验。

| 主题 | 要理解的边界 | 当前覆盖 |
| --- | --- | --- |
| Discovery | 新协议流程不能与旧握手报文混用 | 原生 Client 与原始 HTTP 已实测 |
| MRTR / Listen / Cache 使用策略 | 框架提供能力不等于项目已验证所有交互语义 | 流程与出处；缓存提示字段已实测 |
| Completion | 参数建议，不是模型文本续写 | 概念；未注册 completion handler |
| Pagination | `nextCursor` 不透明，不能当页码 | 概念；清单小，未自建分页 |
| Elicitation | 客户端支持、accept/decline/cancel、表单不收集秘密 | 概念；独立交互实验 G32 暂未实现 |
| Roots / Sampling / Logging | 最新修订弃用但暂未删除；roots 不自动沙箱 | 历史与版本专题 |
| Apps / Skills / Tasks | 扩展协商及 Host 支持范围 | 扩展概览；未增加 UI/扫描器/队列 |
| Authorization / Security | 用户确认、Origin、OAuth、OS 权限不同 | 规范与本地边界讲解 |

验收：能说明哪些行为已通过当前 Client 实测，哪些只是规范对照，哪些仍需独立实验。FastMCP 4 主课程迁移与后续维护见 [版本说明](protocol-versions.md)。

## 综合练习与验证

```powershell
uv run --locked ruff check src tests examples scripts
uv run --locked ruff format --check src tests examples scripts
uv run --locked pytest -o addopts=""
uv build
```

测试覆盖业务输入、schema、Tool 错误、所有教材读取、Prompt 参数、真实传输和清理，并将 FastMCP 兼容弃用警告作为错误。批量运行复验与仓库外 wheel 验收见 [维护脚本](../scripts/README.md)，升级阶段的实测记录见 [检查与升级报告](reports/review-and-upgrade-2026-10-09.md)。

完成学习时应提交：一个能运行的 Server、成功/失败的 Client 结果、实际 MIME/消息角色、传输检查、版本声明和验证记录。新实验优先保持单文件和可观察结果，再决定是否进入主课程。

官方依据：[2026-07-28 基础消息](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)、[HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)、[Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)、[FastMCP 4 Server](https://gofastmcp.com/servers/server)、[Tools](https://gofastmcp.com/servers/tools)、[Resources](https://gofastmcp.com/servers/resources)、[Prompts](https://gofastmcp.com/servers/prompts)、[Clients](https://gofastmcp.com/clients/client)、[3 → 4 迁移](https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3)。本次来源、核对范围与实测证据见 [检查与升级报告](reports/review-and-upgrade-2026-10-09.md)，前一阶段依据保存在 [官网对照报告](archive/2026-10-08/official-docs-gap-analysis-2026-10-08.md)。
