# 协议版本与 FastMCP 4 迁移

更新日期：2026-10-09。主课程已迁移到 FastMCP 4 / SDK 2；下面分别说明依赖、协议与实际验证。项目版本、框架版本、SDK 版本与协议日期不能互相替代。

## 当前运行基线

| 层次 | 依赖范围 / 锁定版本 | 实际含义 |
| --- | --- | --- |
| 项目 | 0.1.0 | 包版本与发现结果中的 Server 版本 |
| Python | >=3.10 / 本地 3.10.18 | FastMCP 4.1.0、SDK 2.3.0 均仍支持 3.10 |
| FastMCP | >=4.1.0,<5 / 4.1.0 | 2026-10-09 PyPI 查询到的最新稳定版 |
| MCP Python SDK | >=2.3.0,<3 / 2.3.0 | SDK 2 原生属性与异常 API |
| Starlette | >=1.3.1,<2 / 1.7.0 | 本地 HTTP 运行栈；保留此前公告修复下限 |
| HTTP Client 依赖 | httpx2 2.13.1 | FastMCP 4 的 HTTP 栈；测试显式声明 dev 依赖 |
| 教学协议 | 2026-07-28 | auto 与固定日期模式实测采用；legacy 实测 2025-11-25 |

FastMCP 4.1.0 是正常 PyPI 依赖，项目已更新 `pyproject.toml` 与 `uv.lock`，通过普通 `uv sync --locked` 安装。没有绕过依赖边界，也没有为双版本编写兼容层。工作区 lock 固定实际版本；用户单独安装 wheel 时按声明范围解析。稳定版不等于以后自动升级：后续同一主版本更新仍需重新锁定和验收。

本地验证平台是 Windows / Python 3.10。lock 为不同 Python/平台包含分支；例如 Python >=3.15 分支当前选择 beartype 0.23.0rc2，当前 3.10 实装为稳定版 0.22.9。不能把本地结果当成所有未来 Python 版本的运行保证。CI 已配置 Windows/Ubuntu Python 3.10，远端执行结果需另查 CI。

## Client 模式与实际观察

| mode | 连接行为 | 对本项目的实测 |
| --- | --- | --- |
| `auto`（默认） | 先探测 `server/discover`；获得现代支持证据时采用现代协议，否则回退旧握手 | 2026-07-28，能取得 Server 身份 |
| `2026-07-28` | 固定现代日期版本，跳过发现 | 2026-07-28，三原语可用；本版本 `server_info` 可为 `None` |
| `legacy` | 显式使用 initialize 握手 | 2025-11-25，保留旧 Client 对照 |

没有 `mode="modern"` API；modern 是协议时代的描述。示例脚本的 `--mode` 接受表中的三个值。

本次原始 discover 的 supportedVersions 仅列 `2026-07-28`；旧握手兼容是通过 legacy 连接另行确认的。框架还默认声明 Logging 与 `io.modelcontextprotocol/ui` 扩展，声明不等于项目已有 UI 页面。当前清单没有 `ui://` Resource，本项目没有开发 Apps 页面/交互工具。实际发现内容见 [wire 记录](evidence/upgrade-2026-10-09/modern-wire.json)。

官方 Client 文档将固定日期模式的 `server_info` 描述为最小合成身份，但本次 4.1.0 实测为 `None`。因此示例按可空属性处理，不依赖其一定含空名字，也不将“没有查询身份”当成调用失败。身份、协议与 instructions 等属性在断开连接后重置，须在 Client 上下文中读取。

```powershell
uv run --locked python examples/client_test.py --mode auto
uv run --locked python examples/client_test.py --mode 2026-07-28
uv run --locked python examples/client_test.py --mode legacy
uv run --locked python examples/transport_client.py stdio --mode auto
```

旧 Host 是否展示 Resource/Prompt、采用何种 JSON/TOML 配置、使用哪个协议仍以其产品支持为准。本次验证的是原生 FastMCP Client 与原始 HTTP，尚未验证具体桌面 Host 的全部交互。

## 新旧协议差异

| 主题 | 2025-11-25 历史流程 | 2026-07-28 当前流程 | 本项目覆盖 |
| --- | --- | --- | --- |
| 生命周期 | initialize → notifications/initialized → 操作；协议 session | 无初始化握手/协议 session，每请求自带 metadata | auto/日期/legacy、stdio/HTTP 实测 |
| Discovery | initialize 交换身份与能力，再查清单 | Server 必须提供 server/discover；Client 可预先查询 | 框架原生 discover 已实测，无普通 Tool 模拟 |
| 请求 metadata | 旧握手参数与可选 metadata | params._meta 中必须有完整前缀的 protocolVersion/clientCapabilities；clientInfo 为 SHOULD | 原始现代 HTTP 请求已实测，完整示例见学习指南 |
| HTTP headers | 旧版 header/session 规则 | MCP-Protocol-Version、Mcp-Method；call/read/get 还须 Mcp-Name，镜像正文 | 无握手调用、HeaderMismatch -32020 已实测 |
| 结果类型 | 未要求 resultType | complete / input_required；扩展可增加类型 | complete 已实测；MRTR 工作流尚未实验 |
| 缓存提示 | 没有这套统一结果字段 | discover/list/read 的 complete 结果必须带 ttlMs/cacheScope | 所有上述方法提示字段已实测；未增加应用缓存策略 |
| MRTR | Server 通过旧连接回调 Client | input_required → 收集补充输入 → 新 id 重试原方法 → complete | 概念；没有交互工作流 |
| 订阅 | resources/subscribe、旧 HTTP GET 流 | subscriptions/listen、subscriptionId 与取消 | 概念；静态教材不推送变化 |
| 结构化结果 | 对象输出与 outputSchema | 可用任意符合 outputSchema 的 JSON 值 | demo 使用对象，已验证结构化结果 |
| SSE 恢复 | Last-Event-ID/session 机制 | 移除旧恢复机制，断流用新 id 重发；副作用需考虑幂等 | 版本专题；没有副作用 Tool |
| Roots / Sampling / Logging | 历史可选能力 | 已弃用但暂未删除，Logging 控制移入每请求 metadata | 带弃用标记的专题 |
| Tasks | 实验性核心能力 | io.modelcontextprotocol/tasks 扩展 | 概览；未注册 Tasks 扩展 |

完整必需 metadata 键名是 `io.modelcontextprotocol/protocolVersion` 与 `io.modelcontextprotocol/clientCapabilities`；没有前缀的普通 `clientCapabilities` 不是替代写法。HTTP 中 Mcp-Name 在 Tool/Prompt 请求来自 name，在资源读取来自 uri；非 ASCII 值需按规范编码。框架 Client 负责这些细节，手工报文不能任意省略。

MRTR 的 requestState 是不透明值，Client 不应解析、修改或假定其内容。input_required 与携带 MRTR 输入的重试不按普通结果缓存。TTL 是新鲜度提示，不是内容永远不变的保证或自动轮询间隔；缓存范围、Origin 检查与身份授权不同。

Roots 只传达相关目录，不会强制文件沙箱。弃用能力最早在 2027-07-28 之后的修订具备移除资格，并非承诺该日删除。

## 已落实的 API 迁移

| 旧写法/行为 | 当前写法/行为 | 原因或验证 |
| --- | --- | --- |
| SDK `McpError` | `from mcp.shared.exceptions import MCPError` | SDK 2 原生导出；不依赖旧命名别名 |
| inputSchema / outputSchema 属性 | input_schema / output_schema | wire JSON 仍是 camelCase；model_dump(by_alias=True) 已验证 |
| uriTemplate / mimeType 属性 | uri_template / mime_type | 示例、测试、指南同步 |
| isError / annotation 属性 | is_error / read_only_hint 等 | 只改 Python 属性；装饰器 annotations 字典保留文档支持的 camelCase 键 |
| httpx HTTP 探针 | httpx2 | FastMCP 4 HTTP 栈与异常类型已变化 |
| 超时消息字符串断言 | MCPError + REQUEST_TIMEOUT | SDK 本地错误码；不冒充规范定义的对端错误 |
| v3 Template MIME 包装 | 直接返回 str + 装饰器 MIME | 4.1.0 实际读取保持 Markdown，删除包装更清楚 |
| 主课程旧握手示例 | metadata / discover / complete / 必需 headers | 旧报文只保留为历史对照 |

当前项目没有 ctx.sample、ctx.sample_step、ctx.list_roots、ctx.elicit、on_initialize 权限钩子、跨调用 Context 状态或旧任务系统，因此无需为这些已删除/受协议时代限制的 API 添加迁移分支。未来 Elicitation 实验应按现代 MRTR/guard 模式设计；ctx.elicit 在默认现代连接不能沿用旧写法。

未知 Tool 在当前 4.1.0 中仍表现为工具错误结果；未知 Resource/非法 Prompt 参数表现为 MCPError。框架的实际异常映射通过测试确认，不从规范分类直接推断具体 Python 异常。

## 历史证据与维护

前一阶段主环境是 FastMCP 3.4.8 / SDK 1.30.0，158 项测试通过；当时在临时副本进行 4.1.0 实验，发现 SDK 改名与 HTTP 依赖差异。该实验绕过了旧主包依赖范围，不代表当时主环境已迁移。

原始实验仍保留：[收集错误](archive/2026-10-09/implementation-2026-10-09/fastmcp4-original-tests.txt)、[调整后的副本测试](archive/2026-10-09/implementation-2026-10-09/fastmcp4-adapted-tests.txt)、[API 探针](archive/2026-10-09/implementation-2026-10-09/fastmcp4-probe.py)、[探针结果](archive/2026-10-09/implementation-2026-10-09/fastmcp4-probe.json)。[前一阶段验收](archive/2026-10-09/implementation-status-2026-10-09.md) 是历史快照，当前状态以 [检查与升级报告](reports/review-and-upgrade-2026-10-09.md) 为准。

后续维护顺序：查 PyPI 与官方迁移指南 → 更新依赖下限/主版本边界 → 正常生成 lock/sync → 改 API 与教材 → Ruff/弃用警告门禁/行为与真实传输测试 → 正常安装仓库外 wheel → 记录版本、证据和未验证范围。可以在现有简单目录中完成，无需额外 providers、数据库或协议兼容层。

复验命令与仓库外安装步骤集中在 [维护脚本](../scripts/README.md)；重复运行的输出写入 `artifacts/`。`docs/evidence/` 中的日期记录和 `docs/archive/` 中的旧实验用于追溯，不作为当前脚本入口。

本次仍未实现独立 Elicitation/MRTR、listen 重连、应用缓存策略、Completion handler、Apps/Skills/Tasks、公开服务 OAuth 或特定 Host 的全部支持。这些是可选实验与部署工作，不是更新 FastMCP 的必要前置条件。

官方依据：[PyPI FastMCP](https://pypi.org/project/fastmcp/)、[SDK](https://pypi.org/project/mcp/)、[3 → 4 迁移](https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3)、[Client](https://gofastmcp.com/clients/client)、[基础消息](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)、[Versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)、[HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)、[Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)、[Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching)、[变更](https://modelcontextprotocol.io/specification/2026-07-28/changelog)。来源查询与内容 hash 见 [本次清单](evidence/upgrade-2026-10-09/official-sources.json)。
