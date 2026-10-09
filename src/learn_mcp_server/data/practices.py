"""练习的专属验收标准；关键词只用于自查，不判断语义正确。"""

from typing import TypedDict


class PracticeTask(TypedDict):
    title: str
    task: str
    checks: list[str]
    checkpoints: dict[str, list[str]]


PRACTICE_TASKS: dict[str, PracticeTask] = {
    "tool": {
        "title": "Tool 练习",
        "task": "实现 get_server_info Tool，并用 Client 发现、调用与检查结果。",
        "checks": [
            "list_tools 可发现工具，说明用途",
            "schema 对应参数，合法/非法输入均验证",
            "通过 Client 检查结果和错误状态",
        ],
        "checkpoints": {
            "控制与用途": ["模型", "model-controlled", "动作"],
            "注册": ["@mcp.tool", "装饰器"],
            "调用与结果": ["call_tool", "tools/call", "schema", "结果"],
        },
    },
    "resource": {
        "title": "Resource 练习",
        "task": "实现 mcp://docs/introduction，区分发现元数据与读取正文。",
        "checks": [
            "list 返回 URI 和 description",
            "read 返回 text 与正确 MIME",
            "未知 URI 反馈明确",
        ],
        "checkpoints": {
            "使用方": ["应用", "application-controlled", "host"],
            "读取入口": ["uri", "read_resource", "resources/read"],
            "内容": ["text", "mime", "正文"],
        },
    },
    "resource-template": {
        "title": "Resource Template 练习",
        "task": "实现 mcp://concepts/{name}，两个名称生成不同资料。",
        "checks": [
            "resources/templates/list 暴露模式",
            "占位符与参数同名",
            "不同值、未知值和查询参数均有明确行为",
        ],
        "checkpoints": {
            "参数映射": ["{name}", "参数", "占位符"],
            "实际读取": ["uri", "read_resource"],
            "动态行为": ["不同", "动态"],
        },
    },
    "prompt": {
        "title": "Prompt 练习",
        "task": "实现 explain_mcp_topic，获取包含 user/assistant 的消息模板。",
        "checks": [
            "prompts/list 描述用途和参数",
            "线上 arguments 是字符串",
            "get 返回 messages，未自动调用模型",
        ],
        "checkpoints": {
            "使用方": ["用户", "user-controlled"],
            "消息": ["messages", "消息", "user", "assistant"],
            "执行边界": ["不调用", "不会自动", "模板"],
        },
    },
    "transport": {
        "title": "Transport 练习",
        "task": "分别从 stdio 子进程和已运行 HTTP 服务调用工具。",
        "checks": ["明确谁启动进程", "真实连接而非仅 Client(mcp)", "设置超时并清理连接/进程"],
        "checkpoints": {
            "本地进程": ["stdio", "子进程"],
            "独立服务": ["http", "独立"],
            "通信": ["管道", "通信", "连接"],
        },
    },
    "json-rpc": {
        "title": "JSON-RPC 练习",
        "task": "写 2026-07-28 请求、成功、错误与通知示意，包含必需 metadata/resultType；HTTP 请求注明对应 headers，旧握手另作对照。",
        "checks": [
            "request 有 id/method/params 与带完整前缀的版本/能力 metadata",
            "response 对应 id，result/error 互斥，完成结果有 resultType",
            "notification 无 id；initialized 只用于旧握手，不混入现代流程",
        ],
        "checkpoints": {
            "请求": ["method", "params", "id"],
            "响应": ["result", "error"],
            "通知": ["无 id", "没有 id", "通知"],
        },
    },
    "config": {
        "title": "Config 练习",
        "task": "生成 stdio/HTTP 配置，并分析一个字段冲突和一个错误类型。",
        "checks": [
            "command/args 与 url 区别清楚",
            "非对象、字段类型和混用被检测",
            "承认 Host 格式不同，不回显秘密",
        ],
        "checkpoints": {
            "stdio": ["command", "args"],
            "HTTP": ["url", "http"],
            "格式边界": ["mcpservers", "host", "格式"],
        },
    },
    "elicitation": {
        "title": "Elicitation 练习",
        "task": "设计选择学习主题的非敏感交互，说明能力支持及三种响应。",
        "checks": [
            "需要客户端声明支持",
            "accept/decline/cancel 均处理",
            "form 不收集 secret，敏感交互用 URL mode",
        ],
        "checkpoints": {
            "能力前提": ["客户端", "能力", "capability"],
            "用户控制": ["accept", "decline", "cancel"],
            "秘密": ["不收集", "敏感", "url mode"],
        },
    },
    "security": {
        "title": "Security 练习",
        "task": "对比用户确认、HTTP Origin、OAuth 与 OS 权限的边界。",
        "checks": [
            "外部输入校验",
            "不把 roots/uvx 当沙箱",
            "Origin 检查不等于身份认证，凭证不回显",
        ],
        "checkpoints": {
            "输入": ["输入校验", "validate"],
            "权限": ["os", "沙箱", "最小权限"],
            "HTTP": ["origin", "授权", "oauth"],
        },
    },
    "debug": {
        "title": "Debug 练习",
        "task": "给连接拒绝、stdout 解析错误、缺依赖各写一条验证动作。",
        "checks": [
            "具体证据优先于 FastMCP 关键词",
            "内存检查与真实传输分层",
            "未知现象列候选并请求证据",
        ],
        "checkpoints": {
            "连接": ["端口", "服务", "连接"],
            "stdio": ["stdout", "stderr"],
            "依赖": ["环境", "import", "module"],
        },
    },
    "tests": {
        "title": "Tests 练习",
        "task": "说明并执行函数、MCP、真实传输、项目外 wheel 四层验证。",
        "checks": [
            "函数与协议结果分别检查",
            "真实 stdio/HTTP 有超时清理",
            "wheel 不依赖仓库相对路径",
        ],
        "checkpoints": {
            "业务与协议": ["函数", "schema", "mcp"],
            "真实传输": ["stdio", "http", "子进程"],
            "分发": ["wheel", "安装", "包"],
        },
    },
    "schema": {
        "title": "Schema 练习",
        "task": "给示例添加默认值、枚举与说明，观察 Client 清单。",
        "checks": [
            "required/default/enum 与函数一致",
            "字段 description 可见",
            "直接调用仍检查业务规则",
        ],
        "checkpoints": {
            "类型": ["schema", "类型"],
            "约束": ["required", "default", "enum", "literal"],
            "业务": ["校验", "验证", "业务"],
        },
    },
    "structured-output": {
        "title": "Structured Output 练习",
        "task": "返回 value 对象，并比较内容块与 Client data。",
        "checks": [
            "outputSchema 与结构化数据一致",
            "content 和 structured_content 均检查",
            "data 不是 wire 字段",
        ],
        "checkpoints": {
            "内容": ["content"],
            "结构": ["structured", "outputschema"],
            "框架": ["data", "fastmcp", "client"],
        },
    },
    "errors": {
        "title": "Errors 练习",
        "task": "调用 divide 成功、分母零、未知工具，分别观察错误。",
        "checks": [
            "业务失败有 is_error",
            "默认 Client 抛 ToolError",
            "区分协议错误与业务错误，记录未知工具在当前框架的实际映射",
        ],
        "checkpoints": {
            "业务": ["iserror", "is_error"],
            "Client": ["toolerror"],
            "协议": ["json-rpc", "协议", "error"],
        },
    },
}

__all__ = ["PRACTICE_TASKS", "PracticeTask"]
