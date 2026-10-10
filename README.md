# learn-mcp-server

`learn-mcp-server` 是一个使用 **FastMCP** 编写的 MCP 学习型 Server。它既是一个可以运行的 MCP Server，也是用于学习 MCP 项目结构、Tool、Resource、Resource Template、Prompt、配置和调试流程的教学示例。

项目以简单清晰为主：主服务提供可查询的教材，独立 demo 展示协议行为，能力通过显式清单注册，教材保存在静态数据中。阅读时可以沿着 `server → registry → tools/resources/prompts → data/utils` 理解调用链。

根目录 README 保留完整的项目介绍、环境准备、安装运行、Host 配置、调试、项目结构和常用命令。更详细的架构、源码阅读顺序、修改入口与后续路线见 [项目架构与后续路线](docs/project-design-and-roadmap.md)，逐课操作和验收见 [学习指南](docs/learning-guide.md)。

## 功能

当前版本提供：

- MCP 核心概念讲解与官方出处。
- FastMCP Tool、Resource、Resource Template、Prompt 示例。
- 学习路线、分级课程资源、练习任务和关键词自查。
- stdio 与 Streamable HTTP 运行、配置和调试说明。
- 常见错误诊断与配置解释。
- FastMCP Client 的内存连接、真实 stdio 和 HTTP 验证示例。
- 独立教学 demo，展示 schema、结构化结果、错误、MIME、消息角色与进度。

当前主服务注册能力：

```text
Tools: 20 个
Resources: 39 个
Resource Templates: 5 个
Prompts: 5 个
```

`check_answer` 是关键词自查，Prompt 返回消息模板；配置解释和诊断处理文本，不执行提交的命令或代码，也不探测配置中的网络目标。

## 环境要求

项目要求 Python >=3.10，推荐使用 **uv** 管理环境和运行命令。工作区的 [.python-version](.python-version) 选择 Python 3.10 系列：

```text
3.10
```

先检查 uv 是否可用：

```powershell
uv --version
```

如果没有安装 uv，Windows PowerShell 可以使用官方安装命令：

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

安装后重新打开终端，再执行 `uv --version`。其他系统和安装方式见 [uv 官方安装说明](https://docs.astral.sh/uv/getting-started/installation/)。

使用 Inspector 还需要 Node.js 和 npx；普通 Server、Client 和测试使用 Python 环境即可。可以通过以下命令检查 Inspector 所需工具：

```powershell
node --version
npx --version
```

## 当前版本

| 层次 | 当前基线 |
| --- | --- |
| 项目 | 0.2.0 |
| Python | >=3.10；工作区选择 3.10 |
| FastMCP | 4.1.0；依赖范围 >=4.1.0,<5 |
| MCP Python SDK | 2.3.0；依赖范围 >=2.3.0,<3 |
| MCP 协议 | 2026-07-28；旧握手作为历史对照 |

依赖范围在 [pyproject.toml](pyproject.toml) 中声明，`uv.lock` 固定工作区实际版本。以下命令使用 `--locked`，保证运行时采用已提交的锁文件。版本来源、Client 模式和迁移差异见 [版本说明](docs/protocol-versions.md)。

## 安装依赖

在项目根目录执行。本文终端示例使用 PowerShell，路径应替换为你本机的位置：

```powershell
cd E:/SoftwareProject/learn-mcp-server
uv sync --locked
uv run --locked python --version
```

`uv sync --locked` 会建立 `.venv/` 并安装项目依赖及开发工具。随后可直接使用 `uv run --locked ...`，无需先手动激活虚拟环境。

## 运行测试

执行全部测试：

```powershell
uv run --locked pytest -q
```

需要查看各测试文件的执行进度时使用：

```powershell
uv run --locked pytest -o addopts=""
```

测试覆盖普通函数、输入校验、MCP 能力发现、Resource/Template MIME、Prompt 参数、demo、真实传输和 Client 生命周期。pytest 将 FastMCP 兼容弃用警告作为错误；[CI](.github/workflows/ci.yml) 还会关闭 camelCase 兼容桥接，并执行构建与仓库外 wheel 验证。

## 主服务与教学 demo

| 服务 | 入口 | 用途 | 代表能力 |
| --- | --- | --- | --- |
| 主服务 | `learn-mcp-server` / `learn_mcp_server.server` | 查询教材、示例、课程、练习、配置和诊断 | `get_server_info`、`explain_concept`、`mcp://docs/introduction` |
| 教学 demo | `learn_mcp_server.demo` / `examples/minimal_server.py` | 观察具体协议行为 | `divide`、`count_steps`、`demo://metadata`、`explain_topic` |

主服务使用 `mcp://...` 资料 URI，demo 使用 `demo://...`。两份 FastMCP 实例独立运行；主服务不会自动提供 demo 的 `divide`。demo 有 2 个 Tools、1 个 Resource、1 个 Resource Template 和 2 个 Prompts。

完整教学源码保存在包内 [demo.py](src/learn_mcp_server/demo.py)，[minimal_server.py](examples/minimal_server.py) 是工作区启动入口。主服务的 `get_code_example` Tool 使用 `{"topic":"minimal-server"}` 可取得完整源码；其他主题中的装饰器片段需要相应 import、mcp 实例和启动入口。

## 本地客户端验证

### 主服务的内存连接

```powershell
uv run --locked python examples/client_test.py
```

[client_test.py](examples/client_test.py) 使用 `Client(mcp)` 连接包内实例，输出 JSON，包含：

- Tools、Resources、Resource Templates 和 Prompts 的发现结果。
- 协议版本与 Server 版本。
- `get_server_info` 的实际返回值。
- 固定 Resource 与 Template 的 MIME。
- Prompt 的消息角色。

它验证内存调用流程；真实进程和网络连接使用下面的传输示例。

### 教学 demo 的内存连接

```powershell
uv run --locked python examples/client_test.py --demo
```

预期看到 `{"value": 3.0}`、JSON Resource、Markdown Template、`user` / `assistant` 两条 Prompt 消息，以及进度 1、2、3。脚本也主动调用零分母检查错误行为，相关 stderr 错误日志属于演示内容。

### 真实 stdio 子进程

```powershell
uv run --locked python examples/transport_client.py stdio --timeout 10
```

[transport_client.py](examples/transport_client.py) 启动主服务子进程，并完成能力发现、Tool 调用、Resource/Template 读取和 Prompt 获取。Client 使用有限超时，并在退出时清理连接和受其管理的 stdio 子进程。

### Client 协议模式

两个 Client 脚本都接受 `--mode auto`（默认）、`--mode 2026-07-28` 和 `--mode legacy`：

```powershell
uv run --locked python examples/client_test.py --mode auto
uv run --locked python examples/client_test.py --mode 2026-07-28
uv run --locked python examples/client_test.py --mode legacy
```

auto 对本项目发现并采用 2026-07-28；固定日期跳过发现，`server_version` 可以为 null，但调用仍可成功；legacy 用于旧握手对照。详细行为见 [版本说明](docs/protocol-versions.md)。

## 本地 stdio 运行

单独启动主服务：

```powershell
uv run --locked learn-mcp-server
```

默认 transport 是 stdio。Server 会等待 Client/Host 发送协议消息，启动后没有普通文本输出是正常状态。stdout 用于 MCP 协议，普通日志应写入 stderr；结束单独启动的服务使用 Ctrl+C。

单独启动教学 demo：

```powershell
uv run --locked python examples/minimal_server.py
```

安装包后也可以通过 `python -m learn_mcp_server.demo` 启动 demo。需要交互观察时使用 Client 或下面的 Inspector。

## Inspector 调试

确认 Node.js/npx 可用后，Windows 下建议使用正斜杠绝对路径，并显式指定 `server.py` 中的 `mcp` 对象：

```powershell
uv run --locked fastmcp dev inspector --no-reload E:/SoftwareProject/learn-mcp-server/src/learn_mcp_server/server.py:mcp
```

把示例路径替换成自己的项目绝对路径，保留 `/`、`:mcp` 和 `--no-reload`。使用正斜杠可以避免 Windows 反斜杠路径在 Inspector URL 转换中的解析歧义。

观察独立教学 demo 时使用：

```powershell
uv run --locked fastmcp dev inspector --no-reload E:/SoftwareProject/learn-mcp-server/src/learn_mcp_server/demo.py:mcp
```

Inspector 连接成功后，查看 Tools、Resources、Resource Templates 和 Prompts，并实际调用 Tool、读取资料、获取消息模板。具体界面标签和协议支持取决于 Inspector 版本。

## stdio 配置

下面使用生态常见的 `mcpServers` JSON。将配置合并到 Host 的 MCP 配置中，保存后按该 Host 的方式重新加载或重启。不同 Host 可能使用 TOML 或专属字段，Resource/Prompt 的展示方式也取决于产品，应以对应 Host 文档为准。

### 本地开发使用

让 Host 直接使用当前工作区代码，推荐先使用 `uv run --locked --directory`：

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--locked",
        "--directory",
        "E:/SoftwareProject/learn-mcp-server",
        "learn-mcp-server"
      ],
      "env": {
        "LEARN_MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

把 `--directory` 后面的路径替换成你本机的项目根目录，先在该目录完成 `uv sync --locked`，并确认 Host 能从 PATH 找到 `uv`。如果找不到，可以把 `command` 换成 uv 可执行文件的绝对路径。

示例文件见 [examples/workspace_stdio_config.json](examples/workspace_stdio_config.json)。JSON 中使用正斜杠可以直接表示 Windows 路径；若使用反斜杠，需要写成 JSON 转义的 `\\`。

### 发布后给别人使用

当前 `0.2.0` 已发布到 [PyPI](https://pypi.org/project/learn-mcp-server/0.2.0/)，可以让 Host 使用 `uvx` 启动。`uvx` 会创建隔离环境并安装依赖，使用者不需要手动指定 Python 解释器路径：

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "learn-mcp-server==0.2.0",
        "learn-mcp-server"
      ]
    }
  }
}
```

示例文件见 [examples/stdio_config.json](examples/stdio_config.json)。这份配置运行已发布的安装包；使用当前源码工作区时选上面的本地开发配置。发布新版本时，应同步包版本和配置中的版本号。

## streamable-http 运行

### 启动 HTTP 主服务

在终端一设置环境变量并启动：

```powershell
$env:LEARN_MCP_TRANSPORT="streamable-http"
$env:LEARN_MCP_HTTP_PORT="8000"
uv run --locked learn-mcp-server
```

默认地址：

```text
http://127.0.0.1:8000/mcp
```

服务固定监听 `127.0.0.1`，端口可以配置为 1–65535。这个 HTTP 入口提供主服务教材，demo 是另一份实例。

### 用 Client 连接

在终端二连接已经运行的服务：

```powershell
uv run --locked python examples/transport_client.py http --url http://127.0.0.1:8000/mcp --timeout 10
```

如果修改了端口，Client URL 和 Host 配置要一起修改。浏览器直接访问 `/mcp` 的结果不能替代 MCP Client 验证；HTTP Client 退出也不会关闭终端一中的独立服务。

### HTTP Host 配置

```json
{
  "mcpServers": {
    "learn-mcp-server-http": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

示例文件见 [examples/streamable_http_config.json](examples/streamable_http_config.json)。先启动 HTTP 服务，再让 Host 连接。框架的 Host/Origin 防护已开启：无效 Origin 返回 403，不可信 Host 返回 421；这些检查与身份授权不同。

### 停止 HTTP 并恢复 stdio

在终端一按 Ctrl+C 停止服务，再清除当前终端的 HTTP 环境变量：

```powershell
Remove-Item Env:\LEARN_MCP_TRANSPORT -ErrorAction SilentlyContinue
Remove-Item Env:\LEARN_MCP_HTTP_PORT -ErrorAction SilentlyContinue
```

之后执行 `uv run --locked learn-mcp-server` 会恢复默认 stdio。

### 环境变量说明

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `LEARN_MCP_TRANSPORT` | `stdio` | 选择 `stdio` 或 `streamable-http` |
| `LEARN_MCP_HTTP_PORT` | `8000` | HTTP 端口，范围 1–65535 |

[.env.example](.env.example) 用于说明配置项，程序不自动读取 `.env`。需要通过终端或 Host 的 `env` 显式传入变量。

## 常用命令

以下命令在项目根目录按需选择执行：

```powershell
# 安装锁定依赖
uv sync --locked

# 执行测试
uv run --locked pytest -q

# 检查主服务、教学 demo 和真实 stdio
uv run --locked python examples/client_test.py
uv run --locked python examples/client_test.py --demo
uv run --locked python examples/transport_client.py stdio

# Inspector 调试，替换为自己的绝对路径
uv run --locked fastmcp dev inspector --no-reload E:/SoftwareProject/learn-mcp-server/src/learn_mcp_server/server.py:mcp

# 代码、格式与依赖检查
uv run --locked ruff check src tests examples scripts
uv run --locked ruff format --check src tests examples scripts
uv pip check

# 批量复验 Client 模式和原始 HTTP
uv run --locked python scripts/verify_runtime.py

# 构建安装包
uv build
```

批量复验的新输出写入被 Git 忽略的 `artifacts/runtime/`。安装包验收另在仓库外独立环境执行，具体步骤见 [维护脚本说明](scripts/README.md)。

## 项目结构

```text
learn-mcp-server/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitattributes
├── .gitignore
├── .github/
│   └── workflows/ci.yml
├── docs/
│   ├── README.md
│   ├── running-and-configuration.md
│   ├── learning-guide.md
│   ├── project-design-and-roadmap.md
│   ├── protocol-versions.md
│   ├── reports/
│   ├── evidence/
│   └── archive/
├── examples/
│   ├── README.md
│   ├── client_test.py
│   ├── transport_client.py
│   ├── minimal_server.py
│   ├── workspace_stdio_config.json
│   ├── stdio_config.json
│   └── streamable_http_config.json
├── scripts/
│   ├── README.md
│   ├── verify_runtime.py
│   └── verify_installed_package.py
├── src/
│   └── learn_mcp_server/
│       ├── __init__.py
│       ├── server.py
│       ├── registry.py
│       ├── settings.py
│       ├── demo.py
│       ├── data/
│       ├── prompts/
│       ├── resources/
│       ├── tools/
│       └── utils/
└── tests/
```

`examples/` 放学习者直接使用的示例，`scripts/` 放维护验收程序，`tests/` 放行为测试。当前指南、最近报告、原始证据和历史记录分别组织在 `docs/` 下。

## 入口说明

| 文件/目录 | 职责 |
| --- | --- |
| [server.py](src/learn_mcp_server/server.py) | 创建主服务 FastMCP 实例，调用注册并按 transport 启动 |
| [registry.py](src/learn_mcp_server/registry.py) | 显式注册 Tools、Resources、Resource Templates 和 Prompts |
| [settings.py](src/learn_mcp_server/settings.py) | 运行常量、环境变量、transport 和端口校验 |
| [demo.py](src/learn_mcp_server/demo.py) | 独立完整教学 Server，展示三原语与进度、错误等行为 |
| [data/](src/learn_mcp_server/data) | 概念、官方出处、课程、练习、代码示例和配置教材 |
| [tools/](src/learn_mcp_server/tools) / [resources/](src/learn_mcp_server/resources) / [prompts/](src/learn_mcp_server/prompts) | 教材查询、资料读取和消息模板函数 |
| [utils/](src/learn_mcp_server/utils) | 小型输入校验与格式化函数 |
| [client_test.py](examples/client_test.py) | 本地内存 Client 验证，可选择主服务或 demo |
| [transport_client.py](examples/transport_client.py) | 真实 stdio/HTTP Client 验证 |
| [verify_runtime.py](scripts/verify_runtime.py) | 批量复验 Client 模式与现代 HTTP |
| [verify_installed_package.py](scripts/verify_installed_package.py) | 在仓库外独立环境验证构建出的 wheel |
| [项目架构](docs/project-design-and-roadmap.md) | 模块职责、源码阅读顺序、修改入口和后续路线 |

## 打包

```powershell
uv build
```

构建产物生成到 `dist/`。以当前 0.2.0 为例：

```text
dist/learn_mcp_server-0.2.0.tar.gz
dist/learn_mcp_server-0.2.0-py3-none-any.whl
```

`dist/` 不提交到 Git。构建完成后，应在仓库外的独立环境正常安装 wheel，再运行 `scripts/verify_installed_package.py` 验收；环境创建、固定依赖导出和安装步骤见 [维护脚本说明](scripts/README.md) 与 [CI 的 wheel 验证步骤](.github/workflows/ci.yml)。

## 发布后运行

当前已发布的 `0.2.0` 可以直接使用：

```powershell
uvx --from learn-mcp-server==0.2.0 learn-mcp-server
```

这也是已发布安装包的 stdio Host 接入方式。构建和本地 Git 提交不会自动发布到 PyPI；当前工作区接入使用前面的 `uv run --locked --directory` 配置。

## 文档与学习顺序

首次使用可以按“安装依赖 → 主服务 Client 验证 → demo 验证 → 真实传输/Inspector → 阅读源码”的顺序操作。

| 目标 | 文档 |
| --- | --- |
| 查看完整运行、环境变量与接入说明 | [运行与配置](docs/running-and-configuration.md) |
| 按课程操作并观察、验收结果 | [学习指南](docs/learning-guide.md) |
| 理解架构、模块职责与后续改进 | [项目架构与后续路线](docs/project-design-and-roadmap.md) |
| 理解 FastMCP/SDK API、Client 模式与新旧协议 | [版本说明](docs/protocol-versions.md) |
| 选择学习示例和维护脚本 | [示例目录](examples/README.md)、[维护脚本](scripts/README.md) |
| 查找全部指南、报告和历史记录 | [文档目录](docs/README.md) |
| 查看当前依赖升级的检查结果 | [检查与升级报告](docs/reports/review-and-upgrade-2026-10-09.md) |
| 追溯原始依据与较早阶段 | [检查证据](docs/evidence/README.md)、[历史记录](docs/archive/README.md) |

报告中的版本、测试数、命令和环境记录对应其检查日期；日常使用按当前 README 和指南操作。历史证据继续保留，重复验证的临时输出写入 `artifacts/`。
