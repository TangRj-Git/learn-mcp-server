# 项目架构与后续路线

更新日期：2026-10-09。本文描述实际代码；改造前的计划与问题依据保存在 [官网对照报告](archive/2026-10-08/official-docs-gap-analysis-2026-10-08.md)。

## 定位与运行基线

`learn-mcp-server` 帮助学习者观察 Tool、Resource、Resource Template、Prompt 的注册、发现、使用和失败行为。主服务是可查询的教材，`demo.py` 是可执行的三原语实验，两者分别创建 FastMCP 实例。

主课程使用 FastMCP 4.1.0、SDK 2.3.0 和 MCP 2026-07-28。旧握手作为历史对照；MRTR 等可选交互专题与实际已验证能力分开说明，详见 [版本说明](protocol-versions.md)。项目版本 0.2.0 与协议日期含义不同。

## 一条清楚的调用链

```text
命令行/Host
   → server.main / create_server
   → registry.register_all(FastMCP 实例)
   → tools / resources / prompts 的普通函数
   → data 的静态教材 + utils 的校验/格式化
```

| 模块 | 实际职责 | 阅读重点 |
| --- | --- | --- |
| `server.py` | 创建带版本和 instructions 的实例，调用注册，选择 transport | factory 返回独立实例；不将注册结果写入模块 globals |
| `registry.py` | 20 Tools、39 Resources、5 Templates、5 Prompts 的显式清单 | 查名字与 URI；函数直接注册，声明 Markdown MIME |
| `settings.py` | stdio/HTTP 选择、本地端口、协议教学常量 | 读取环境变量；不自动读取 .env |
| `tools/` | 概念查询、示例、配置校验、练习自查、诊断 | 输入校验与可解释结果；不执行提交的代码/命令 |
| `resources/` | 从同一教材数据生成正文 | list 元数据与 read 内容不同；保留已有 URI/别名 |
| `prompts/` | 生成可复用消息模板 | 说明参数、限定 level/days、拒绝空输入 |
| `data/` | 概念、官方出处、三等级课程、按主题练习、示例 | 版本与核对日期；不在运行时抓取网页 |
| `utils/` | 通用非空、选择、列表、URL 校验与格式化 | 小函数，不隐藏业务分支 |
| `demo.py` | 独立完整示例 | schema、结构化结果、错误、MIME、查询参数、多消息、进度 |

现代 discovery/metadata、旧握手兼容、消息解析、HTTP/SSE、schema 生成由 FastMCP/SDK 完成。注册清单直接引用普通函数，函数测试直接从所属模块导入；公开 Server 入口是 `create_server()`、`mcp`、`main()`。

FastMCP 4.1.0 的 Template 普通字符串返回已保留声明的 MIME，实测读取是 `text/markdown`。已移除前一阶段 v3 所需的 `_markdown_template` 与显式内容项包装，注册流程更直接。原 v3 证据保留在历史报告中。

## 源码阅读顺序与修改入口

建议先运行 demo，再沿一条具体能力读代码：

1. [demo.py](../src/learn_mcp_server/demo.py)：在同一文件看到三原语的定义、装饰器和启动入口。
2. [server.py](../src/learn_mcp_server/server.py) 与 [settings.py](../src/learn_mcp_server/settings.py)：理解主服务如何创建和启动。
3. [registry.py](../src/learn_mcp_server/registry.py)：找到主服务能力对应的函数、名字和 URI。
4. 以 `explain_concept` 为例，读 [concept_tools.py](../src/learn_mcp_server/tools/concept_tools.py) → [concepts.py](../src/learn_mcp_server/data/concepts.py) / [references.py](../src/learn_mcp_server/data/references.py)，再读 [concept_resources.py](../src/learn_mcp_server/resources/concept_resources.py)，观察 Tool 和 Resource 怎样复用正文。
5. [client_test.py](../examples/client_test.py) → [test_mcp_integration.py](../tests/test_mcp_integration.py) → [transport_client.py](../examples/transport_client.py)：从能力使用走到协议断言和真实传输。

| 想修改的内容 | 首先修改哪里 | 需要一起检查什么 |
| --- | --- | --- |
| 概念正文、官方出处 | `data/concepts.py`、`data/references.py` | 对应 Tool/Resource 输出、版本标记与练习 |
| 课程顺序、练习和自查点 | `data/curriculum.py`、`data/practices.py` | `tools/practice_tools.py` 与三个等级的目标、操作、验收 |
| 完整教学示例及新示例片段 | `demo.py`、`data/examples.py` | 包内完整源码和片段提取、`tests/test_demo.py`、`test_examples.py` |
| 主服务的 Tool/Resource/Prompt | 对应 `tools/`、`resources/`、`prompts/` 模块，再更新 `registry.py` | 名字/URI、schema、MIME、消息和能力数；README 与发现测试 |
| 启动参数、Host 配置 | `settings.py`、`.env.example`、`examples/*_config.json` | `data/configs.py` 教材、运行指南、设置与传输测试 |
| 依赖版本或验收流程 | `pyproject.toml`、`uv.lock`、`scripts/`、`.github/workflows/ci.yml` | 版本说明、测试、真实传输与仓库外安装 |

新增能力继续使用普通函数和显式注册。修改教材已有主题通常只需调整数据；只有需要新的行为或新的公开能力时才增加函数与注册项。

## 教材怎样保持一致

1. 概念正文在 `data/concepts.py`，工具讲解与资源读取共用。`data/references.py` 记录官方页面、版本标签和实际核对日。
2. 课程、计划和衔接使用小型静态数据表。不同等级的目标、操作和验收不同，学习路线结束于 `tests`。
3. 练习按主题保存检查点。`check_answer` 只展示关键词匹配与缺失，语义质量由人工与实际运行判断。
4. 完整代码与新片段从包内 `demo.py` 读取/提取。安装 wheel 后仍能取得源码，不依赖仓库 `examples/` 路径。
5. `examples/` 放学习用 Client、demo 入口和 Host 配置；`scripts/` 放运行复验与安装验收。已安装包可通过 `python -m learn_mcp_server.demo` 或内置 Resource 获取完整示例。

修改正文时同时检查版本标签、引用和对应练习；修改完整示例时通过 Client 验证观察结果。

当前操作说明集中在四份 [指南](README.md)。最近报告放在 `docs/reports/`，其原始证据放在 `docs/evidence/`；较早报告与证据按阶段放在 `docs/archive/`。临时复验输出放在被 Git 忽略的 `artifacts/`，便于保留报告证据的原始内容。

## 本地运行边界

stdio 由 Client 管理子进程，stdout 只用于协议。HTTP 主服务固定 loopback，端口可配置，框架 Host/Origin 防护已开启。连接服务使用协议客户端，不能用浏览器 GET 的结果判断服务是否可用。

配置解释器校验 JSON 对象、字段类型、command/url 冲突和 HTTP URL 格式，隐藏 args/env/URL query 的值；校验不连接目标。URL 格式合法也不证明目标安全或可达。

Prompt 的代码/错误文本作为待分析资料，获取模板不执行内容、不调用模型。用户确认、Origin、OAuth 和操作系统权限是不同边界。相关内容作为课程讲解，不新增认证服务。

## 验证分层

| 层次 | 验证内容 | 文件/命令 |
| --- | --- | --- |
| 普通函数 | 输入边界、分级计划、检查点、诊断优先级 | `tests/test_regressions.py` 等 |
| 内存 MCP | 能力元数据、schema、结果、MIME、Prompt、进度 | `tests/test_mcp_integration.py`、`test_demo.py` |
| 生命周期/真实传输 | 超时、取消退出清理；stdio 子进程；HTTP 防护 | `test_client_lifecycle.py`、`test_transports.py` |
| 安装包 | 仓库外导入、完整代码、Resource、demo | `scripts/verify_installed_package.py` |

Ruff 负责基础错误、导入和格式；pytest 负责行为并将 FastMCP 兼容弃用警告作为错误；uv.lock 负责工作区依赖可复现。CI 配置 Windows/Ubuntu，本地新版执行证据见 [检查与升级报告](reports/review-and-upgrade-2026-10-09.md)。

## 后续路线

| 内容 | 当前状态 | 继续工作的触发条件 |
| --- | --- | --- |
| 主课程三原语、错误、参数、传输 | 已有完整示例及验证 | 发现具体学习障碍或依赖行为变化 |
| 2026 新规范 | discovery、metadata、结果与缓存提示字段已实测；MRTR/listen/cache 使用策略仍是专题 | 有独立学习需求时增加小型交互实验 |
| FastMCP 4 | 已迁入主依赖；使用 SDK 2 原生属性与 httpx2 | 新稳定版发布时更新 lock 并重跑验收 |
| Completion / Pagination | 概念覆盖 | 清单规模或学习任务需要时，先用框架公开 API |
| Elicitation（G32） | 概念覆盖，独立交互实验尚未实现 | 确定支持该能力的 Client/Host 并明确 accept/decline/cancel 验收 |
| Apps / Skills / Tasks | 可选扩展概览 | 出现独立学习目标与明确的 Host 支持范围 |
| HTTP 远程部署/授权 | 本地边界与规范讲解 | 明确真实部署需求后单独设计与验收 |

保持现有目录和显式清单即可。没有当前需求支持添加数据库、队列、课程状态服务、动态插件扫描、LLM 判卷、前端框架或自写 JSON-RPC 解析器。新增教学实验优先一份小型可运行文件与对应验证，并避免影响主服务的学习路径。
