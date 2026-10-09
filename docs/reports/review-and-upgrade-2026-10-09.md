# 项目详细复查与 FastMCP 4 升级报告

核对日期：2026-10-09。检查对象是当前工作区 `learn-mcp-server`，包括此前尚未提交的改造结果。本次保留原有改进与历史证据，在现有目录中继续修复和升级。

归档说明：本文记录 FastMCP 4 升级阶段的检查结果，测试数、环境和证据均对应该阶段。后续内容整理将报告放入 `reports/`、原始记录放入 `evidence/`、维护程序放入 `scripts/`；导航链接和下方复验命令已同步，原始证据保留当时内容。当前操作入口见 [文档目录](../README.md)。

## 1. 结论

项目确实还存在输入边界、诊断规则和配置解释上的错误，已复现并修复。FastMCP 已从前一阶段的 3.4.8 升到 **4.1.0**，MCP Python SDK 从 1.30.0 升到 **2.3.0**，主课程同步采用 **2026-07-28** 协议。4.1.0 是本次 PyPI 查询到的最新稳定版，不是预发布版本。

当前主服务的注册清单仍为 **20 Tools / 39 Resources / 5 Templates / 5 Prompts**。教材仍为 42 个概念、15 个示例主题、14 个练习主题；独立 demo 为 2 Tools / 1 Resource / 1 Template / 2 Prompts。

验证结果：185 项测试通过；Ruff 与 30 个源码文件的限定范围 Mypy 检查通过；11 个 Client 命令组合成功；原始现代 HTTP 请求成功；wheel/sdist 构建与仓库外正常安装成功；72 个当前运行依赖未检出已知漏洞。

这些结果证明本次检查覆盖的启动、核心能力、输入回归与传输路径可用，不构成“所有环境与所有输入永远没有错误”的保证。具体未验证范围在第 8 节列明。

## 2. 依据与检查范围

本次使用三类证据，不把推测当成已确认问题：

| 证据 | 用途 | 保存位置 |
| --- | --- | --- |
| PyPI 当前元数据 | 确认版本、Python 下限、预发布与撤回状态 | [FastMCP](../evidence/upgrade-2026-10-09/fastmcp-metadata.json)、[SDK](../evidence/upgrade-2026-10-09/mcp-metadata.json)、[httpx2](../evidence/upgrade-2026-10-09/httpx2-metadata.json) |
| 官方规范/迁移文档 | 确认 API、协议与必需字段规则 | [43 个页面的来源清单](../evidence/upgrade-2026-10-09/official-sources.json)、[关键原文摘录](../evidence/upgrade-2026-10-09/official-excerpts.md) |
| 当前源码与真实运行 | 判断实际错误、框架映射和安装行为 | 回归测试、[pytest 输出](../evidence/upgrade-2026-10-09/pytest.txt)、[CLI 输出](../evidence/upgrade-2026-10-09/cli-runtime.json)、[wire 报文](../evidence/upgrade-2026-10-09/modern-wire.json) |

来源清单包含 URL、请求的 Markdown URL、响应状态、实际地址、时间与 SHA-256。43 个选定页面均成功返回，核对的是与当前教材/迁移有关的内容，不声称逐行审计了整个官网。官网文档和实际版本表现不一致时，明确记录两者并以当前实测决定代码处理。

源码检查覆盖入口/配置、显式注册、全部 Tools/Resources/Prompts、教材与完整示例、输入校验、测试、依赖声明/lock、打包和 CI。没有运行用户提交的代码、命令或配置目标；工具仍处理静态教材与文本。

前一阶段报告保留：[原项目审计](../archive/2026-10-08/project-audit-2026-10-08.md)、[官网差距 G01–G34](../archive/2026-10-08/official-docs-gap-analysis-2026-10-08.md)、[v3 实施快照](../archive/2026-10-09/implementation-status-2026-10-09.md)。这些文件中的旧基线/测试数描述历史阶段，当前状态以本文与 [版本说明](../protocol-versions.md) 为准。

## 3. 实际错误与修复

下面“修复前”指本次检查中的实际探针或代码验证结果；修复后行为由列出的回归测试确认。严重程度按学习项目影响判断，这些静态格式/诊断错误不是已证实的外部系统攻击。

| 编号 | 具体触发与修复前表现 | 影响 | 当前修复与证据 |
| --- | --- | --- | --- |
| R01 | `http://example.com/#` 的空 fragment 被当成无 fragment | 与 URL 校验器自己的限制不一致 | 检查任何字面 `#`，有内容/空 fragment 都拒绝；`test_http_config_rejects_invalid_urls` |
| R02 | URL 路径中的字面 DEL `\x7f`、C1 `\x80` 未被拒绝 | “合法 URL”提示不准确 | 拒绝 C0、DEL/C1 与空白；保持百分号编码与自定义 endpoint 的正常支持；同一 URL 回归测试 |
| R03 | hostname 使用去除全部尾部点的处理，接受 `example.com..` | 把无效主机解释为有效配置 | 最多去除一个合法终止点，保留标签长度/字符校验；同一 URL 回归测试 |
| R04 | 错误码 `4044` 因包含 `404` 被诊断为 HTTP 404 | 引导学习者排查错误层次 | 404 使用数字边界匹配；真实 `HTTP 404 Not Found` 仍给 HTTP 候选方向；`test_debug_rules_require_specific_evidence` |
| R05 | 单独的 `print`、`stdio` 或 `security` 触发 stdout/Resource 诊断 | 给出缺少证据的结论 | stdout 证据、URI/resource 单词边界、配置字段与普通 JSON 分开；仅 stdio 时说明进程证据不足；相关诊断回归测试 |
| R06 | ImportError 消息含 `REQUEST_TIMEOUT`，或 stdio 启动上下文含缺模块错误时，按普通关键词先判超时/输出问题 | 掩盖真正的导入错误 | 明确的 import/module 错误优先于超时、stdio 等上下文词；`test_actual_import_error_wins_over_stdio_context` 与诊断参数化测试 |
| R07 | 配置 `type="http"` 配合 command、`type="stdio"` 配合 url，显式类型被忽略；SSE 配置被称为 Streamable HTTP | 配置解释与实际意图冲突 | 校验 type 类型/非空与对应字段，拒绝冲突；未知 Host 类型说明范围；SSE 标为旧 HTTP+SSE；`test_explicit_transport_type_is_not_silently_ignored` |
| R08 | 新增 type 处理将 `Any | None` 直接传给声明接收 str 的函数，Mypy 报错 | 类型契约不清楚 | 增加显式 isinstance 检查，异常反馈仍清楚；[Mypy 输出](../evidence/upgrade-2026-10-09/mypy.txt) |
| R09 | 升级后的指南/练习仍使用 v3/SDK1 基线、旧 Python 属性与旧握手主流程 | 示例可能失败，学习者混用两套协议 | README、指南、版本/架构文档、概念/课程/练习和 Prompt 基线同步；现代主课有 metadata/resultType/headers，旧握手明确为历史 |

修复代码：[validators.py](../../src/learn_mcp_server/utils/validators.py)、[debug_tools.py](../../src/learn_mcp_server/tools/debug_tools.py)、[config_tools.py](../../src/learn_mcp_server/tools/config_tools.py)。回归依据：[test_regressions.py](../../tests/test_regressions.py)。

没有把以下情况误报成项目错误：

- URL 使用自定义路径而非 `/mcp`：协议允许，本项目仅默认 `/mcp`。
- Python/Node/二进制作为 stdio command：有效，uv/uvx 是推荐工具。
- 未实现全部可选扩展：学习项目无须因此增加服务层、队列或数据库。
- 未知主题返回帮助页：这是主服务的明确策略，demo 则抛错误，均避免静默换成另一主题。
- JSON 重复键：Python json.loads 会保留后项；本解释器尚未增加重复键拒绝，不能因此声称已实现完整 Host 配置验证。

## 4. 最新版本为什么能用、具体怎么迁移

### 4.1 正常依赖组合

| 层次 | 迁移前阶段 | 当前实际版本 / 声明范围 |
| --- | --- | --- |
| FastMCP | 3.4.8 / `<4` | 4.1.0 / `>=4.1.0,<5` |
| MCP Python SDK | 1.30.0 / `<2` | 2.3.0 / `>=2.3.0,<3` |
| HTTP 栈 | httpx / httpcore | httpx2 2.13.1 / httpcore2 2.13.1 |
| Starlette | 1.7.0 | 1.7.0 / `>=1.3.1,<2` |
| Python | 3.10.18 | 工作区 3.10.18；独立安装 3.10.19；项目仍要求 >=3.10 |
| 协议主课 | 2025-11-25 | 2026-07-28；legacy 对照采用 2025-11-25 |

FastMCP 4.1.0 的包依赖同版本 fastmcp-slim；SDK 2 引入独立 mcp-types。主依赖仍使用熟悉的 fastmcp 包，不额外设计 slim/extras 组合。Python 无须为此次升级强制改成 3.11。

工作区通过正常 `uv lock` / `uv sync --locked` 解析安装，wheel 也按声明范围与导出的 lock 正常安装，未使用安装 `--no-deps` 绕过依赖。当前 lock 共 89 个包条目，包含开发依赖和 Python/平台分支；该数字不是当前运行依赖数。当前平台审计的非开发依赖是 72 个。

### 4.2 不是只改一个版本号

| 迁移差异 | 已完成的处理 |
| --- | --- |
| SDK 2 不再从旧导入路径导出 `McpError` 名字 | 测试改用原生 `MCPError` |
| SDK Python 属性从 camelCase 改为 snake_case | 示例/测试/指南改为 input_schema、output_schema、uri_template、mime_type、is_error 和 annotation 属性 |
| wire JSON 仍使用 camelCase | 不改线上 inputSchema/outputSchema 等字段；by_alias=True 序列化已验证 |
| HTTP 栈迁移 | HTTP 探针改用 httpx2，调试识别 httpx2.ReadTimeout，明确 dev 依赖 |
| 超时异常文案变化 | 断言本地 MCPError 与 REQUEST_TIMEOUT，不绑定文案；不把 SDK 本地码当作规范对端错误 |
| Template MIME 行为变化 | 4.1.0 直接返回 str 已保持装饰器 MIME，删除 v3 的 `_markdown_template` 包装与显式内容项适配 |
| 默认 Client 转为现代协议 | 主教材与原始 HTTP 测试采用 discovery/每请求 metadata/complete/必需 headers |
| fixed-date 模式跳过 discovery | server_info 按可空处理，CLI 输出 null 有清楚说明 |
| 兼容桥接可能掩盖旧写法 | pytest 将 FastMCPDeprecationWarning 当错误；本地和 CI 关闭 camelCase 兼容桥接 |

装饰器 annotations 字典仍使用官方接受的 `readOnlyHint` / `openWorldHint` 键。它们不是旧 Python 属性访问，不能机械地改成另一组字段。

项目没有使用 ctx.sample/ctx.sample_step/ctx.list_roots/ctx.elicit、on_initialize 权限钩子、跨调用 Context 状态或旧 Tasks API，所以没有引入旧新版兼容分支。新增 Elicitation 时必须依据现代 MRTR/guard 模式设计，不能直接照搬旧 ctx.elicit 示例。

## 5. 现代协议与框架行为的实测

| 检查点 | 本次实际结果 | 依据 |
| --- | --- | --- |
| auto 模式 | 内存、真实 stdio、真实 HTTP 均为 2026-07-28，得到 Server 0.1.0 身份 | CLI + 参数化传输测试 |
| 固定日期模式 | 同样成功使用 2026-07-28，跳过发现，server_version 为 null | CLI + 内存/真实传输测试 |
| legacy 模式 | 2025-11-25，三原语仍可用，HTTP initialize 返回正确版本/身份 | CLI + 参数化传输/legacy initialize 测试 |
| server/discover | 无 initialize 即可使用；有 complete、身份、能力与 supportedVersions | [modern-wire.json](../evidence/upgrade-2026-10-09/modern-wire.json) |
| 原始现代 HTTP | 每请求 `_meta` + 协议/方法/名称 headers；调用、资源读取成功，无 mcp-session-id | raw HTTP 测试 + wire 记录 |
| header 与正文不一致 | HTTP 400，JSON-RPC HeaderMismatch -32020 | `test_http_modern_mismatched_tool_header_returns_protocol_error` |
| 缓存提示 | discover、四种 list、resources/read 的 complete 结果都有非负 ttlMs 与 public/private scope；当前采样为 0/private | 原始 HTTP 测试 + wire 记录 |
| Markdown Template | 声明和实际读取均为 text/markdown | 全部教材/模板读取、demo 测试 |
| Tool 错误映射 | divide 零分母返回 is_error；默认 Client 抛 ToolError；未知 Tool 当前也被框架映射为工具错误结果 | demo 测试 |
| Resource / Prompt 错误 | 未知 demo 主题、非法查询 bool、非法 Prompt 天数为 MCPError | demo 测试 |
| 进度 | 1、2、3 三次事件；Context 不在模型输入 schema | demo 测试 + CLI |
| HTTP 防护 | 外部/伪造/空 Origin 403，不可信 Host 421；无 Origin 与本地 Inspector Origin 成功 | 真实 HTTP 测试 |
| 超时/取消退出清理 | 无副作用等待 Tool 退出连接后执行 finally；不声称超时立即停止任意业务或回滚 | 生命周期测试 |

### 两个容易误读的观察

**固定日期模式的身份**：官网 Client 文档描述最小合成身份，本次 4.1.0 的 server_info 实测可为 None。示例遵守可空属性契约；需要身份时采用 auto。现代协议版本不是靠是否有 Server 身份来判断。

**框架默认能力**：discover 的 supportedVersions 本次仅列 2026-07-28；旧协议支持通过 legacy 另行证明。FastMCP 4.1.0 同时默认声明 Logging 与 UI 扩展，源码明确默认合并 `io.modelcontextprotocol/ui`。本项目没有 ui:// 资源与 Apps 页面，因此不会将这个默认声明写成“项目已开发 Apps”。没有为隐藏框架声明而使用私有修改或不存在的构造参数。依据：[实际 discover](../evidence/upgrade-2026-10-09/modern-wire.json)、[版本固定的框架源码摘录](../evidence/upgrade-2026-10-09/framework-capabilities.txt)。

完整教学请求与 headers 在 [学习指南](../learning-guide.md)。`mode="modern"` 不是有效 API：使用 auto、日期字符串或 legacy。

## 6. 架构仍以简单清晰为主

```text
server → registry → tools / resources / prompts → data / utils
demo.py：独立完整示例
examples/：学习 Client、demo 入口与配置
scripts/：运行复验与安装验收
tests/：函数、协议、传输与生命周期
```

入口继续只创建/注册/启动。registry 保持显式清单，函数直接注册，去掉此前针对 v3 MIME 的包装。没有动态扫描、数据库、队列、课程状态服务、LLM 判卷、前端工程或自写 JSON-RPC 解析器。

现代 metadata/HTTP/旧握手兼容由 FastMCP 与 SDK 处理；项目只为其编写观察与回归测试。配置解释器仍是指定 JSON 格式的静态教学工具，不执行命令、不验证目标可达性，也不保证支持所有 Host 格式。args/env/query 的值被隐藏，但它不是对任意文本的通用凭证识别器。

教材的完整示例继续来自包内 demo.py，wheel 安装后仍可获取；不依赖仓库相对 examples 路径。Prompt 继续生成消息模板，check_answer 继续明确限定为关键词自查。

## 7. 验证记录

| 验证 | 结果 | 落盘证据 |
| --- | --- | --- |
| Ruff check | 通过 | [ruff-check.txt](../evidence/upgrade-2026-10-09/ruff-check.txt) |
| Ruff format --check | 46 个源码/测试/示例文件通过 | [ruff-format.txt](../evidence/upgrade-2026-10-09/ruff-format.txt) |
| Mypy | 30 个源码文件通过；follow-imports=skip / ignore-missing-imports，不等于检查第三方库内部 | [mypy.txt](../evidence/upgrade-2026-10-09/mypy.txt) |
| pytest | 185 passed；关闭兼容桥接并启用弃用警告门禁 | [pytest.txt](../evidence/upgrade-2026-10-09/pytest.txt) |
| 主工作区依赖完整性 | 78 个安装包检查通过 | [pip-check.txt](../evidence/upgrade-2026-10-09/pip-check.txt) |
| CLI | 主服务的内存/stdio/HTTP × 三模式；demo 的 auto/legacy，共 11 组成功 | [cli-runtime.json](../evidence/upgrade-2026-10-09/cli-runtime.json)、[探针源码](../evidence/upgrade-2026-10-09/runtime-probe.py) |
| 现代 wire | 4 组原始 HTTP 报文保存；测试另覆盖全部缓存提示方法与 header 错误 | [modern-wire.json](../evidence/upgrade-2026-10-09/modern-wire.json) |
| 构建 | sdist 与从 sdist 构建的 wheel 成功 | [build.txt](../evidence/upgrade-2026-10-09/build.txt) |
| 仓库外安装 | 新虚拟环境正常解析安装 73 个包（72 个运行依赖 + 项目）；无 editable/PYTHONPATH 泄漏，pip check、三原语、包内示例、真实 stdio 成功 | [wheel-install-and-check.txt](../evidence/upgrade-2026-10-09/wheel-install-and-check.txt)、[环境](../evidence/upgrade-2026-10-09/environment.json) |
| 依赖已知漏洞审计 | PyPI 服务检查当前平台 72 个固定运行依赖，0 已知漏洞、无跳过；不包含未来公告保证 | [完整 runtime 导出](../evidence/upgrade-2026-10-09/runtime-requirements.txt)、[pip-audit JSON](../evidence/upgrade-2026-10-09/pip-audit-runtime.json) |
| 文档与教材 | 当前/历史顶层文档的本地链接与 JSON/Python/HTTP 报文代码块可解析，内置示例/配置代码块可解析，git diff --check 通过 | [document-check.json](../evidence/upgrade-2026-10-09/document-check.json) |
| CI 配置 | Windows/Ubuntu Python 3.10，锁定安装、检查、真实传输、demo、构建和仓库外 wheel；兼容桥接关闭 | [ci.yml](../../.github/workflows/ci.yml)；未声称远端已运行 |

漏洞审计使用临时 pip-audit 工具，读取完整固定 runtime 导出；其中审计器的 `--no-deps --disable-pip` 仅避免再次解析已固定列表，**不是**项目安装绕过依赖的做法。实际 wheel 安装始终正常解析依赖。

复跑常规检查：

```powershell
uv sync --locked
uv run --locked ruff check src tests examples scripts
uv run --locked ruff format --check src tests examples scripts
$env:FASTMCP_MCP_CAMELCASE_COMPAT="false"
uv run --locked pytest -o addopts=""
uv run --locked python examples/client_test.py --demo
uv run --locked python scripts/verify_runtime.py
uv pip check
uv build
```

仓库外验证脚本是 [verify_installed_package.py](../../scripts/verify_installed_package.py)，CI 提供创建环境/导出/正常安装/执行的完整步骤。探针会创建临时 HTTP 子进程并在 finally 清理。本次运行结束后未发现遗留的该项目 Server/Client 进程。

## 8. 后续改进与实际限制

| 优先级 | 当前状态/建议 | 触发条件与简单实现方式 |
| --- | --- | --- |
| 维护 | 同一 FastMCP/SDK 主版本保留更新空间，lock 保持可复现 | 新稳定版本发布或具体兼容问题出现时，查迁移指南、更新 lock、同步教材、重跑当前验收 |
| 维护 | 本地是 Windows Python 3.10.18，独立安装 3.10.19；其他平台尚未本地执行 | 使用 CI 检查 Ubuntu；确需新 Python 时再增加测试矩阵，不先增加抽象层 |
| 维护 | lock 的 Python >=3.15 分支选择 beartype 0.23.0rc2；当前 3.10 实装稳定 0.22.9 | 在声称支持新 Python 前审查分支与实测，不把当前结果推广到未来解释器 |
| 可选教学 | Elicitation/MRTR 独立交互实验 G32 尚未实现 | 用一份小型 guard 示例验证客户端支持与 accept/decline/cancel，保持非敏感输入 |
| 可选教学 | listen 重连与应用缓存策略未验证；只检查了提示字段 | 有明确订阅/缓存学习目标时增加独立实验；无需 Redis 或事件平台 |
| 可选教学 | Completion/Pagination 是概念，未注册自定义 completion handler | 需要参数建议或大清单时使用框架公开 API |
| 可选扩展 | Apps/Skills/Tasks 没有项目级功能/工作流 | 明确 Host 支持与学习目标后独立实验，不为“最新”强行引入 UI/扫描器/任务系统 |
| 部署 | 本地 loopback + Host/Origin 防护已实测；没有公开服务 OAuth 方案 | 确定真实远程服务需求后单独设计授权/部署，不把 Origin 当身份认证 |
| 接入 | Inspector CLI 参数已确认，具体 Inspector UI/桌面 Host 全流程未验收 | 指定 Host 与版本后实际连接；配置格式/Resource/Prompt 展示以产品支持为准 |
| 输入工具 | 配置讲解有格式范围，诊断仍是启发式规则 | 新真实错误出现时先复现，再加针对性的分支；不把候选方向称为根因分析 |

本次没有将代码提交/推送、发布 PyPI、创建 PR 或部署外部服务。改动与报告均保留在当前工作区供审阅。

## 9. 主要官方依据

- [FastMCP 3 → 4 迁移](https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3)：SDK 2、属性、HTTP 栈、已删除/受时代限制的 API。
- [FastMCP Client](https://gofastmcp.com/clients/client)：auto/date/legacy 模式、属性生命周期与可空身份。
- [Tools](https://gofastmcp.com/servers/tools)、[Resources](https://gofastmcp.com/servers/resources)、[Prompts](https://gofastmcp.com/servers/prompts)：当前注册与结果接口。
- [MCP 基础消息](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)、[Versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)：每请求 metadata、结果类型与新旧时代。
- [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)：必需 headers、镜像字段与 HeaderMismatch。
- [Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)、[Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching)：发现与缓存提示要求。
- [2026-07-28 变更](https://modelcontextprotocol.io/specification/2026-07-28/changelog)、[扩展](https://modelcontextprotocol.io/extensions/overview)：已弃用能力与可选扩展边界。

判断项目错误以当前源码和复现为依据；判断规范/API 变化以对应版本官方文档为依据；判断“当前可用”以本次真实运行与安装证据为依据。
