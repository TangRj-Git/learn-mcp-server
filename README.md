# learn-mcp-server

`learn-mcp-server` 是一个使用 **FastMCP** 编写的 MCP 学习型 Server。它既是一个可以运行的 MCP Server，也是一个用于学习 MCP 项目结构、Tool、Resource、Resource Template、Prompt、配置和调试流程的教学示例。

这个仓库的根目录 README 只保留项目介绍、安装运行、Host 配置和常用命令。更完整的需求设计、开发路线和模块拆分说明已经移动到 [docs/project-design-and-roadmap.md](docs/project-design-and-roadmap.md)。

## 功能

当前版本提供：

- MCP 核心概念讲解
- FastMCP Tool / Resource / Resource Template / Prompt 示例
- 学习路线、课程资源和练习任务
- stdio 与 streamable-http 配置说明
- 常见错误诊断和调试建议
- FastMCP Client 集成验证脚本

当前注册能力：

```text
Tools: 20 个
Resources: 39 个
Resource Templates: 5 个
Prompts: 5 个
```

## 环境要求

推荐使用 `uv` 管理项目环境和运行命令。

```powershell
uv --version
```

如果没有安装 `uv`，Windows PowerShell 可以使用：

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

项目 Python 版本由 [.python-version](.python-version) 固定为：

```text
3.10
```

## 安装依赖

在项目根目录执行：

```powershell
uv sync
```

## 运行测试

```powershell
uv run pytest -q
```

## 本地客户端验证

```powershell
uv run python examples\client_test.py
```

该脚本会列出当前 MCP Server 暴露的 Tools、Resources、Resource Templates 和 Prompts，并调用 `get_server_info` 做一次基本验证。

## Inspector 调试

```powershell
uv run fastmcp dev inspector src\learn_mcp_server\server.py
```

## stdio 配置

### 发布后给别人使用

发布到 PyPI 后，推荐让 Host 使用 `uvx` 启动。`uvx` 会创建隔离环境并自动安装依赖，使用者不需要手动配置 Python 解释器路径。

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "learn-mcp-server==0.1.0",
        "learn-mcp-server"
      ]
    }
  }
}
```

示例文件见 [examples/stdio_config.json](examples/stdio_config.json)。

### 本地开发使用

如果还没有发布到 PyPI，或者想让 Host 直接使用当前工作区代码，可以使用 `uv run --directory`：

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "E:\\SoftwareProject\\learn-mcp-server",
        "learn-mcp-server"
      ]
    }
  }
}
```

把 `--directory` 后面的路径替换成你本机项目根目录。

## streamable-http 运行

PowerShell：

```powershell
$env:LEARN_MCP_TRANSPORT="streamable-http"
uv run learn-mcp-server
```

默认地址：

```text
http://127.0.0.1:8000/mcp
```

对应 Host 配置示例见 [examples/streamable_http_config.json](examples/streamable_http_config.json)。

恢复 stdio：

```powershell
Remove-Item Env:\LEARN_MCP_TRANSPORT
```

## 常用命令

```powershell
uv sync
uv run pytest -q
uv run python examples\client_test.py
uv run fastmcp dev inspector src\learn_mcp_server\server.py
uv build
```

## 项目结构

```text
learn-mcp-server/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── docs/
│   └── project-design-and-roadmap.md
├── examples/
│   ├── client_test.py
│   ├── stdio_config.json
│   └── streamable_http_config.json
├── src/
│   └── learn_mcp_server/
│       ├── server.py
│       ├── registry.py
│       ├── settings.py
│       ├── data/
│       ├── prompts/
│       ├── resources/
│       ├── tools/
│       └── utils/
└── tests/
```

## 入口说明

- [src/learn_mcp_server/server.py](src/learn_mcp_server/server.py)：创建 FastMCP 实例并启动服务
- [src/learn_mcp_server/registry.py](src/learn_mcp_server/registry.py)：集中注册 Tools、Resources、Resource Templates 和 Prompts
- [src/learn_mcp_server/settings.py](src/learn_mcp_server/settings.py)：运行配置和 transport 选择
- [examples/client_test.py](examples/client_test.py)：本地 FastMCP Client 验证脚本
- [docs/project-design-and-roadmap.md](docs/project-design-and-roadmap.md)：完整项目需求、设计和开发路线

## 打包

```powershell
uv build
```

构建产物会生成到 `dist/`，该目录不会提交到 Git。

## 发布后运行

发布到 PyPI 后，可以直接用：

```powershell
uvx --from learn-mcp-server==0.1.0 learn-mcp-server
```

这也是推荐写入 MCP Host 配置的运行方式。
