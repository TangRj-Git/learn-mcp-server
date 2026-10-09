"""教学正文的单一数据源；运行时不联网更新。"""

from typing import TypedDict

CONCEPTS: dict[str, str] = {
    "mcp": """
MCP，全称 Model Context Protocol，是模型应用连接外部工具、数据和提示词的协议。
MCP Server 不等于大模型；FastMCP 是 Python 框架；Host 是使用能力的应用。
先运行最小 Server，再用 Client 发现、调用、读取和获取模板。
""",
    "host": """
Host 管理模型、MCP Client、上下文与用户交互。
它决定哪些 Resource 加入上下文、何时使用用户选择的 Prompt，如何呈现 Tool 确认。
Host 确认不会自动限制本地 Server 的操作系统权限。
""",
    "client": """
Client 是 Host 内负责协议通信的组件。
当前 2026-07-28 无初始化握手；每次请求带版本与客户端能力 metadata。
FastMCP 4 Client 默认 mode="auto"，探测 server/discover 后使用 modern，旧服务回退 legacy。
2025-11-25 的 initialize/notifications/initialized 是历史流程；可显式 mode="legacy" 对照，固定现代版用 mode="2026-07-28"。
""",
    "server": """
Server 提供 Tools、Resources 和 Prompts，通过能力声明与清单供 Client 发现。
它可以是 Client 管理的 stdio 子进程，也可以是独立 HTTP 服务。
本项目查询内置数据和生成文本，不执行提交的代码、命令或网络请求。
""",
    "tool": """
Tool 是 MCP Server 暴露给模型调用的可执行能力（model-controlled）。
它适合动作、计算、查询，用 @mcp.tool() 注册；类型和 docstring 形成 schema 与说明。
模型提出调用不代表已授权。call_tool 返回 content、可选 structuredContent 和错误状态。
""",
    "resource": """
Resource 是可读取上下文，典型使用由应用控制（application-controlled）。
resources/list 返回 URI、说明和 MIME 等元数据；resources/read 返回实际 contents。
内容可为 text 或 blob；Host 决定怎样加入模型上下文，不会自动进入对话。
""",
    "prompt": """
Prompt 是 Server 定义、用户选择使用的消息模板（user-controlled），用 @mcp.prompt() 注册。
prompts/get 返回 user/assistant 消息，不会自动调用模型。
协议 arguments 是字符串；FastMCP 可以转换成函数声明的 int 等类型。
""",
    "resource-template": """
Resource Template 用 URI 参数动态读取，如 mcp://concepts/{name} 对应函数参数 name。
遵循 RFC 6570，resources/templates/list 列模式，resources/read 使用展开后的实际 URI。
FastMCP 4 的必需参数应在路径中，{?limit} 查询参数须有默认值，变量须对应函数参数。
普通 str 返回保留装饰器声明的 MIME；未知值与编码通过实际读取检查。
mcp:// 是资源标识，不是 HTTP /mcp 服务地址。
""",
    "transport": """
Transport 传递 JSON-RPC：stdio 用子进程管道，Streamable HTTP（streamable-http）用 HTTP 和可选 SSE。
先判断 Server 由 Client 启动还是独立运行。传输方式和协议版本是两个维度。
Client(mcp) 的内存检查验证注册/API，不验证进程、端口或网络。
""",
    "stdio": """
stdio 通过标准输入和标准输出通信，Client 通常启动并管理 Server 子进程。
stdout 只能写协议消息；普通日志写 stderr，不要使用 print 污染 stdout。
Python、Node、二进制均可启动；uv/uvx 是推荐方式，非协议要求。
虚拟环境只隔离依赖，不提供操作系统权限沙箱。
""",
    "streamable-http": """
Streamable HTTP 连接已运行服务，支持 JSON 或 SSE 响应，不是普通 REST API。
浏览器打开 /mcp 不能代替 Client 验证，需正确方法、媒体类型和 header。
2026-07-28 请求须有 MCP-Protocol-Version、Mcp-Method；call/read/get 还须有匹配 name/uri 的 Mcp-Name。
本项目监听 127.0.0.1 并开启 Host/Origin 检查；无效 Origin 返回 403。
localhost 不是身份认证边界，公开受限服务仍需授权设计。
""",
    "sse": """
SSE（Server-Sent Events）是 HTTP 持续传递事件的编码技术。
旧 HTTP+SSE 传输已弃用，但 Streamable HTTP 仍可用 SSE，两者不能混同。
2026-07-28 删除 Last-Event-ID 恢复，断流后用新 id 重发；副作用操作需考虑幂等。
""",
    "json-rpc": """
JSON-RPC 2.0 请求有 jsonrpc、id、method、params；响应关联相同 id。
成功有 result，失败有 error，不能同时出现；通知没有 id，不等待 response。
2026-07-28 请求 params._meta 必须包含 io.modelcontextprotocol/protocolVersion 与 io.modelcontextprotocol/clientCapabilities。
普通成功结果带 resultType="complete"；通知无 id。任意 JSON 输出不等于合法 MCP 消息。
""",
    "lifecycle": """
当前 2026-07-28：可先 server/discover，然后 list/call/read/get；每请求 metadata 包含版本和能力。
无需 initialize/initialized 或协议 session；能力不是某次先前请求建立的隐含状态。
2025-11-25 的 initialize → initialized → 操作属于历史。Client 可用 auto、日期版本或 legacy；没有 mode="modern" 选项。
capabilities 描述类别，list 方法返回具体清单；进程/连接的生命周期不是对话生命周期。
""",
    "capability-negotiation": """
当前能力协商/声明：2026-07-28 用每请求 _meta 声明客户端能力，server/discover 返回服务能力与支持版本。
capabilities 不返回全部工具 schema；具体清单另用 list 方法。
旧 initialize 交换能力是 2025-11-25 历史流程。未声明的能力不能被 Server 擅自假定。
""",
    "notification": """
通知是没有 id、无需返回 result 的 JSON-RPC 消息，表达进度或状态变化。
请求相关进度与独立资源/清单订阅不同；旧 subscribe 与新 listen 见 subscriptions。
""",
    "schema": """
inputSchema 描述 Tool 输入，outputSchema 描述结构化结果。
类型、默认值、Literal、Annotated/Field 都影响声明；框架默认允许某些兼容类型转换。
SDK 2 在 Python 中读取 input_schema/output_schema；wire 字段仍是 inputSchema/outputSchema。
schema 正确不代表业务合法；直接 Python 调用不自动运行注册验证，业务仍需校验。
""",
    "structured-output": """
Python return、MCP content/structuredContent 和 Client result.data 属于不同层。
content 是内容块，structuredContent 是机器可读结果，outputSchema 约束结构。
result.data 是 FastMCP 便利接口，不是 wire 字段。示例用对象；当前协议允许任意符合 schema 的 JSON 值。
MCP 结构化结果不等于模型的结构化生成。
""",
    "errors": """
JSON-RPC error 是协议层失败，Tool 执行失败通常用结果 isError 表达。
Client 默认对工具错误抛 ToolError；raise_on_error=False 可读 result.is_error。
Python 异常、wire 错误和 Client 异常不同。检查状态与结构，不只看关键词。
错误信息应可理解，不回显内部堆栈、路径或凭证。
""",
    "context": """
Context 是 FastMCP 框架对象，不是 MCP wire 类型；用 CurrentContext() 注入。
ctx 不在模型可填写的 inputSchema 中，可用于 report_progress 等调用相关操作。
简单计算用同步函数；async 不自动创造异步 I/O。
""",
    "progress": """
进度与请求关联，Client progress_handler 接收 progress、total、message。
ctx.report_progress 显式报告；Client 需请求进度，不自动建立后台 Task。
示例只模拟三个确定步骤，不访问网络、不长时间 sleep。
""",
    "cancellation": """
超时控制等待，取消是合作行为，不保证已发生的副作用回滚。
写文件或网络提交等动作重试时需幂等；示例优先纯计算。
退出或取消仍须清理连接和子进程。
""",
    "logging": """
普通 stderr 日志与 MCP 协议 Logging 不同；stdio stdout 必须保持协议格式。
Logging 在 2026-07-28 已弃用但保留；删除 logging/setLevel，改用请求 _meta 的 io.modelcontextprotocol/logLevel 控制。
主课程不要求协议 logging，本地排查仍可写 stderr。
""",
    "sampling": """
采样是旧版 Server 请求客户端模型生成的可选能力，需客户端支持和用户控制。
Sampling 在 2026-07-28 已弃用，暂未删除，新实现不优先采用。
FastMCP 4 移除 ctx.sample/ctx.sample_step；本项目保留历史讲解，不增加 LLM 依赖。
""",
    "roots": """
根目录（Roots）是客户端告知 Server 的相关目录/文件信息，不是访问控制。
协议不强制 Server 留在 roots 内，不提供自动文件系统沙箱；限制靠 OS、沙箱或路径检查。
2026-07-28 已弃用但保留，新实现优先用 Tool 参数、Resource URI 或配置传递目录。
""",
    "elicitation": """
Elicitation 请求用户补充信息，需客户端支持；Host 负责交互，Server 不得假设已同意。
区分 accept、decline、cancel；form mode 不收集密码、API key、token、支付凭证。
敏感交互用 URL mode，明确目标域名与导航同意；第三方交互与 MCP 访问 OAuth 不同。
新版用 MRTR，FastMCP 4 的 ctx.elicit 受协议时代限制。本项目先讲概念。
""",
    "authorization": """
Authorization 主要规范 HTTP 访问授权，是可选能力，支持时按相应 OAuth 规范实现。
stdio 凭证通过环境等方式提供，不套用 HTTP OAuth；用户确认 Tool 与 token 授权不同。
新版优先 Client ID Metadata Documents，DCR 已弃用；本项目不自建授权服务。
""",
    "security": """
安全边界包括外部输入、用户数据、OS 权限、HTTP 身份与 Host 确认。
外部资料可能有 prompt injection，文字界定数据不保证消除攻击。
uvx、roots、用户确认均不自动限制 OS 权限；Origin 检查不是身份授权。
本项目保持静态查询、最小权限和本地监听。
""",
    "tasks": """
Tasks 用于持续跟踪长时间运行工作。2025-11-25 中是实验性核心能力。
2026-07-28 转为官方扩展 io.modelcontextprotocol/tasks，tasks/get 轮询、tasks/update 补输入，移除旧 tasks/result/list。
普通 async Tool 或进度不等于 Task；本项目快查询无需队列或持久状态。
""",
    "config": """
mcpServers JSON 是生态常见格式，不是所有 Host 必须使用的协议标准。
stdio 用 command/args 启动，HTTP 用 url 连接，不能混用；具体 Host 格式查对应产品官网。
uv/uvx 是推荐，Python/Node/二进制也可以。解释器不执行命令、不探测 URL、不回显凭证。
""",
    "debug": """
先定位注册逻辑、进程启动、协议传输或 Host 展示的哪一层失败。
连接拒绝查服务/端口，stdout JSON 错误查普通输出，ModuleNotFoundError 查环境，URI 错误查映射。
先内存 Client，再真实 stdio/HTTP；只含 FastMCP 字样不足以判断依赖故障。
""",
    "tests": """
测试分四层：普通函数、MCP schema/结果、真实 stdio/HTTP、仓库外 wheel。
内存 Client 不验证网络，关键词不证明结论。检查状态、结构、主题关联与可运行示例。
uv run --locked pytest；传输检查设超时并清理子进程，不机械追求 100% 覆盖率。
""",
    "completion": """
completion/complete 提供 Prompt/Template 参数建议，不是 LLM 文本续写。
ref/prompt 或 ref/resource 指明对象，values 最多 100 项，可带 total/hasMore。
需声明 completions 和 Client 支持；本项目先讲概念，不侵入 SDK 私有 handler。
""",
    "pagination": """
list 结果的 nextCursor 指向下一批，后续请求用 cursor；游标不透明，不能当页码。
清单很小无需自写引擎，独立实验可用框架 list_page_size。
""",
    "latest-protocol": """
2026-07-28 删除 initialize/initialized 与协议 session，每请求 _meta 带版本和客户端能力。
新增 discover、MRTR、subscriptions/listen、ttlMs/cacheScope，结果有 resultType。
当前主课程使用 FastMCP 4.x / SDK 2.x；modern 连接已验证，MRTR 等可选交互仍需独立实验。
""",
    "discovery": """
2026-07-28 Server 必须实现 server/discover，Client 可选择预先调用。
返回版本、能力、身份，具体 Tool schema 仍查 tools/list；不能手工注册为普通 Tool。
当前 Server 由 FastMCP 实现 discover，Client 默认 auto 探测并使用 modern；legacy 保留历史兼容。
""",
    "mrtr": """
MRTR：原请求 → input_required → Client 收集输入 → 用新 id 重试原方法 → complete。
inputRequests/inputResponses 传递补充输入，requestState 是不透明字符串，Client 不解析或修改。
替代当前协议的独立 Server 回调；本项目只讲流程，不宣称已实现 MRTR 交互工作流。
""",
    "subscriptions": """
2026-07-28 用 subscriptions/listen 订阅资源/清单变化，subscriptionId 关联并可取消。
旧 resources/subscribe 和 HTTP GET 流属于历史章节，请求进度不是独立订阅。
资料不会在进程内变化，主服务不推送课程变更。
""",
    "caching": """
当前规范要求 discover/list/资源读取的 complete 结果携带 ttlMs 与 cacheScope 提示，分别表示新鲜度与 public/private 范围。
ttlMs=0 表示立即过期，TTL 不承诺内容不变，也不是自动轮询间隔；框架提供字段，不必自建缓存服务。
input_required 和带 MRTR 输入的重试不按普通缓存复用。缓存范围不是授权。
解释语义即可，不引入 Redis。
""",
    "extensions": """
扩展在核心之外定义能力，需协商并取决于 Host/Client 支持。
Tasks、Apps、Skills、Auth 扩展不是所有 Server 必须实现的功能。
Roots/Sampling/Logging 2026-07-28 已弃用但保留，最早在 2027-07-28 后修订具备移除资格。
""",
    "apps": """
MCP Apps 用 UI Resource 与沙箱 iframe 展示交互界面，有额外 UI 消息与权限。
属于可选扩展，需查客户端支持矩阵；本项目优先三原语，不增加前端框架。
""",
    "skills": """
官方扩展 io.modelcontextprotocol/skills 提供 skills/list/get，文件用 resources/read。
manifest 描述 SKILL.md 和支持文件的 URI、大小与 hash；需扩展协商与客户端支持。
本项目只讲概览，不扫描本地技能目录。
""",
}


class LearningModule(TypedDict):
    name: str
    topics: list[str]
    description: str


LEARNING_MODULES: list[LearningModule] = [
    {
        "name": "MCP 基础概念",
        "topics": ["mcp", "host", "client", "server"],
        "description": "区分协议、框架和宿主。",
    },
    {
        "name": "MCP 原语",
        "topics": ["tool", "resource", "resource-template", "prompt"],
        "description": "运行并观察三种原语。",
    },
    {
        "name": "MCP 传输方式",
        "topics": ["transport", "stdio", "streamable-http", "sse"],
        "description": "内存检查与真实通信。",
    },
    {
        "name": "MCP 协议消息",
        "topics": [
            "json-rpc",
            "lifecycle",
            "capability-negotiation",
            "schema",
            "structured-output",
            "errors",
        ],
        "description": "输入、结果与失败行为。",
    },
    {
        "name": "MCP 进阶能力",
        "topics": [
            "context",
            "progress",
            "cancellation",
            "notification",
            "completion",
            "pagination",
            "elicitation",
            "sampling",
            "roots",
            "logging",
            "tasks",
        ],
        "description": "标版本的可选能力和历史专题。",
    },
    {
        "name": "MCP 安全与授权",
        "topics": ["security", "authorization"],
        "description": "确认、HTTP 授权与 OS 权限。",
    },
    {
        "name": "MCP 工程化实践",
        "topics": ["config", "debug", "tests"],
        "description": "配置、排查与包验证。",
    },
    {
        "name": "最新规范与扩展",
        "topics": [
            "latest-protocol",
            "discovery",
            "mrtr",
            "subscriptions",
            "caching",
            "extensions",
            "apps",
            "skills",
        ],
        "description": "当前 modern 协议；可选专题与项目实际能力分开。",
    },
]

CONCEPT_COMPARISONS = {
    ("tool", "resource"): [
        ("使用控制", "模型提出调用", "应用选择上下文"),
        ("输入", "tools/call arguments", "resources/read uri"),
        ("输出", "content / structuredContent / isError", "contents: text 或 blob"),
        ("示例", "计算两数之和", "读取学习资料"),
    ],
    ("resource", "resource-template"): [
        ("发现", "resources/list 列固定 URI", "resources/templates/list 列 URI 模式"),
        ("读取", "固定 URI", "展开参数后的 URI"),
    ],
    ("prompt", "tool"): [
        ("使用控制", "用户选择模板", "模型提出调用"),
        ("输入", "线上字符串参数", "schema 定义的 JSON 值"),
        ("输出", "user/assistant messages", "执行结果与错误"),
    ],
    ("stdio", "streamable-http"): [
        ("启动", "Client 管理子进程", "服务独立运行"),
        ("通信", "stdin/stdout", "HTTP/可选 SSE"),
        ("检查", "命令、环境、stdout", "endpoint、header、Origin"),
        ("退出", "清理子进程", "Client 退出不等于关服务"),
    ],
    ("host", "client"): [
        ("职责", "管理模型、界面和上下文", "执行协议通信"),
        ("关系", "管理多个 Client", "连接相应 Server"),
    ],
}

__all__ = ["CONCEPTS", "CONCEPT_COMPARISONS", "LEARNING_MODULES", "LearningModule"]
