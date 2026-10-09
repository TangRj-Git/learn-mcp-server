# learn-mcp-server

用于学习 MCP 的 Python Server。主服务提供可查询的教材，独立 demo 展示 Tool、Resource、Resource Template 和 Prompt 的实际行为。代码保持显式注册与静态数据，适合沿调用链阅读。

## 快速开始

需要 Python >=3.10 和 [uv](https://docs.astral.sh/uv/getting-started/installation/)。在项目根目录执行：

```powershell
uv sync --locked
uv run --locked python examples/client_test.py
uv run --locked python examples/client_test.py --demo
```

第一条 Client 命令检查主服务，第二条检查教学 demo。它们使用内存连接；真实 stdio、HTTP、Inspector 与 Host 接入见 [运行与配置](docs/running-and-configuration.md)。

demo 预期得到 `{"value": 3.0}`、Markdown Template、user/assistant 两条 Prompt 消息和进度 1、2、3；它主动检查零分母，相关 stderr 错误日志属于演示内容。

## 两个服务，各有用途

| 服务 | 入口 | 学习用途 |
| --- | --- | --- |
| 主服务 | `learn-mcp-server` / `learn_mcp_server.server` | 查询概念、示例、课程、练习、配置与诊断 |
| 教学 demo | `learn_mcp_server.demo` / `examples/minimal_server.py` | 计算、schema、结构化结果、错误、MIME、Prompt 消息与进度 |

主服务的能力清单：

```text
Tools: 20 个
Resources: 39 个
Resource Templates: 5 个
Prompts: 5 个
```

主服务使用 `mcp://...` 资料 URI；demo 使用 `demo://...`，并提供 `divide` / `count_steps`。两份实例独立运行，具体操作见 [学习指南](docs/learning-guide.md)。

## 当前版本

| 层次 | 当前基线 |
| --- | --- |
| 项目 | 0.1.0 |
| Python | >=3.10 |
| FastMCP | 4.1.0；依赖范围 >=4.1.0,<5 |
| MCP Python SDK | 2.3.0；依赖范围 >=2.3.0,<3 |
| MCP 协议 | 2026-07-28；旧握手作为历史对照 |

`uv.lock` 固定工作区依赖。版本来源、Client 模式和迁移差异见 [版本说明](docs/protocol-versions.md)。

## 从哪里开始阅读

| 目标 | 入口 |
| --- | --- |
| 启动服务、连接 HTTP、配置 Host/Inspector | [运行与配置](docs/running-and-configuration.md) |
| 按课程操作并观察结果 | [学习指南](docs/learning-guide.md) |
| 看懂模块职责、调用链和后续路线 | [项目架构](docs/project-design-and-roadmap.md) |
| 理解当前 API、新旧协议与升级方法 | [版本说明](docs/protocol-versions.md) |
| 查找审计报告、原始依据与历史记录 | [文档目录](docs/README.md) |

## 项目目录

```text
src/learn_mcp_server/  Server、显式注册、教材与完整 demo
examples/             学习用 Client、demo 入口和 Host 配置
scripts/              运行验证与安装包验收
tests/               函数、MCP、真实传输与生命周期测试
docs/                 当前指南、报告、证据与历史归档
.github/workflows/    CI 检查
```

调用链：`server → registry → tools/resources/prompts → data/utils`。先读 [server.py](src/learn_mcp_server/server.py) 与 [registry.py](src/learn_mcp_server/registry.py)，再选一个能力沿着其函数和教材数据阅读。

[示例目录](examples/README.md) 区分主服务与 demo；[维护脚本](scripts/README.md) 说明如何验收；[架构文档](docs/project-design-and-roadmap.md) 给出完整源码阅读顺序。

## 检查与构建

```powershell
uv run --locked ruff check src tests examples scripts
uv run --locked ruff format --check src tests examples scripts
uv run --locked pytest -o addopts=""
uv pip check
uv build
```

[CI](.github/workflows/ci.yml) 执行检查、真实传输、构建和仓库外 wheel 验证。当前依赖升级的证据见 [检查与升级报告](docs/reports/review-and-upgrade-2026-10-09.md)。

`check_answer` 是关键词自查，Prompt 返回消息模板；配置解释和诊断处理文本，不执行提交的命令/代码或探测目标网络。环境变量说明见 [.env.example](.env.example)，程序不自动加载 `.env`。
