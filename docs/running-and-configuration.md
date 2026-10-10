# 运行与配置

本文集中说明安装、启动和接入。逐课学习见 [学习指南](learning-guide.md)，API/协议版本见 [版本说明](protocol-versions.md)。以下命令在项目根目录运行，终端示例使用 PowerShell。

## 安装与第一次连接

需要 Python >=3.10，推荐使用 [uv](https://docs.astral.sh/uv/getting-started/installation/)：

```powershell
uv sync --locked
uv run --locked python examples/client_test.py
uv run --locked python examples/client_test.py --demo
```

`client_test.py` 默认连接主服务，`--demo` 连接教学实例。两者使用 `Client(mcp)` 内存连接，输出能力清单、协议版本、结果、MIME 和消息角色。

| 观察 | 主服务 | 教学 demo |
| --- | --- | --- |
| Python 模块 | `learn_mcp_server.server` | `learn_mcp_server.demo` |
| Tool 示例 | `get_server_info`、`explain_concept` | `divide`、`count_steps` |
| Resource URI | `mcp://docs/introduction` 等 | `demo://metadata`、`demo://topics/tool` |
| 能力数：Tool / Resource / Template / Prompt | 20 / 39 / 5 / 5 | 2 / 1 / 1 / 2 |

完整教学源码是包内 [demo.py](../src/learn_mcp_server/demo.py)。其他装饰器片段需要其 import、mcp 实例和启动入口；`get_code_example("minimal-server")` 返回完整源码。

## stdio：由 Client 管理子进程

连接真实主服务子进程：

```powershell
uv run --locked python examples/transport_client.py stdio --timeout 10
```

单独启动主服务使用 `uv run --locked learn-mcp-server`，默认 transport 为 stdio；教学 demo 使用：

```powershell
uv run --locked python examples/minimal_server.py
```

安装包后也可使用 `python -m learn_mcp_server.demo`。单独启动的 stdio 服务会等待协议输入，不应在终端输入普通聊天文本。普通日志写 stderr，stdout 只传协议。

## HTTP：先启动服务，再连接

终端一启动主服务：

```powershell
$env:LEARN_MCP_TRANSPORT="streamable-http"
$env:LEARN_MCP_HTTP_PORT="8000"
uv run --locked learn-mcp-server
```

终端二连接已经运行的服务：

```powershell
uv run --locked python examples/transport_client.py http --url http://127.0.0.1:8000/mcp --timeout 10
```

HTTP 入口提供主服务教材；demo 是另一份实例。浏览器直接打开 `/mcp` 不能替代协议 Client 检查。

服务固定监听 `127.0.0.1`；默认端口 8000，允许配置为 1–65535。框架 Host/Origin 防护开启：非法 Origin 为 403，不可信 Host 为 421；合法无 Origin 请求与本地 Inspector Origin 可通过。这些检查与公开服务的身份授权不同。

Ctrl+C 结束服务后，恢复终端默认 stdio 设置：

```powershell
Remove-Item Env:\LEARN_MCP_TRANSPORT -ErrorAction SilentlyContinue
Remove-Item Env:\LEARN_MCP_HTTP_PORT -ErrorAction SilentlyContinue
```

[.env.example](../.env.example) 只说明变量，程序不自动加载 `.env`。Client 默认等待 10 秒并用 `async with` 清理连接；HTTP Client 退出不关闭独立服务，取消不保证副作用回滚。

## Inspector

需要 Node.js/npx。Windows 替换为自己的绝对路径，使用正斜杠、显式 `:mcp` 和 `--no-reload`：

```powershell
uv run --locked fastmcp dev inspector --no-reload E:/SoftwareProject/learn-mcp-server/src/learn_mcp_server/server.py:mcp
```

观察 demo 时把最后的路径改为 `src/learn_mcp_server/demo.py:mcp` 的绝对路径。连接后查看 Tools、Resources、Templates、Prompts 并实际调用/读取。Inspector 支持的协议与展示取决于其版本。

## Host 配置

| 场景 | 示例文件 | 使用前准备 |
| --- | --- | --- |
| 当前源码工作区，推荐先使用 | [workspace_stdio_config.json](../examples/workspace_stdio_config.json) | 替换项目绝对路径，确认 Host 能找到 uv |
| 连接已启动的本地 HTTP 主服务 | [streamable_http_config.json](../examples/streamable_http_config.json) | 按上面步骤先启动服务 |
| 已发布安装包的 uvx 接入 | [stdio_config.json](../examples/stdio_config.json) | `0.2.0` 已发布到 [PyPI](https://pypi.org/project/learn-mcp-server/0.2.0/)；确认 Host 能找到 uvx |

这些文件使用生态常见的 `mcpServers` JSON。Host 可能使用 TOML 或专属格式，Resource/Prompt 展示也取决于产品；具体配置查 Host 文档。Python、Node、可执行文件都是有效 stdio command，uv/uvx 是推荐工具。

## Client 模式

两个 Client 脚本支持 `--mode auto`（默认）、`--mode 2026-07-28`（固定日期）、`--mode legacy`（旧握手），没有 `--mode modern`。

auto 对本项目发现并采用现代协议。固定日期跳过发现，`server_version` 可以为 null，但调用仍可成功。版本属性应在 Client 上下文中读取；详细对照和原始 HTTP metadata/headers 示例见 [版本说明](protocol-versions.md) 与 [学习指南](learning-guide.md)。
