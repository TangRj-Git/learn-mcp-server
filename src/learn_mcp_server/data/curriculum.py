CURRICULUMS = {
    "beginner": """
# MCP Beginner 课程

学习目标：
用最短路径理解 MCP 是什么，并能运行、观察、调用一个最小 MCP Server。

第 1 课：MCP、Host、Client、Server
- 理解 MCP 不是模型本身，而是模型应用连接外部能力的协议。
- 读取 mcp://docs/introduction 和 mcp://docs/architecture。
- 练习 explain_concept("mcp") 和 get_concept_map()。

第 2 课：Tool
- 理解 Tool 是模型可以调用的动作。
- 读取 mcp://docs/tools 和 mcp://examples/basic-tool。
- 练习 get_practice_task("tool")，再用 check_answer 检查理解。

第 3 课：Resource
- 理解 Resource 是模型可以读取的上下文。
- 读取 mcp://docs/resources 和 mcp://examples/basic-resource。
- 对比 compare_concepts("tool", "resource")。

第 4 课：Prompt
- 理解 Prompt 是可复用任务模板。
- 读取 mcp://docs/prompts 和 mcp://examples/basic-prompt。
- 调用 explain_mcp_topic 观察 Prompt 返回结构。

第 5 课：Inspector 和客户端验证
- 使用 uv run fastmcp dev inspector src\\learn_mcp_server\\server.py 查看能力列表。
- 运行 examples/client_test.py，确认 Tools、Resources、Prompts 都能被发现。
""",
    "intermediate": """
# MCP Intermediate 课程

学习目标：
掌握动态资源、配置生成、传输方式和端到端 Client 调用流程。

第 1 课：Resource Template
- 理解 Resource Template 是带参数的动态 Resource。
- 读取 mcp://docs/resource-template 和 mcp://examples/resource-template。
- 练习 get_practice_task("resource-template")。

第 2 课：Transport
- 对比 stdio 和 streamable-http。
- 读取 mcp://docs/stdio、mcp://docs/streamable-http 和 mcp://docs/config-local-vs-remote。
- 调用 compare_local_and_remote_config()。

第 3 课：Host 配置
- 调用 generate_stdio_config(command, args) 生成本地配置。
- 调用 generate_http_config(server_url) 生成 HTTP 配置。
- 用 explain_config(config_text) 解释配置。

第 4 课：端到端 Client
- 读取 mcp://examples/end-to-end-client。
- 理解 list_tools、list_resources、call_tool、read_resource、get_prompt 的顺序。

第 5 课：JSON-RPC
- 读取 mcp://docs/json-rpc。
- 练习 get_practice_task("json-rpc")。
""",
    "advanced": """
# MCP Advanced 课程

学习目标：
理解 MCP 进阶能力、边界和真实项目排查方式。

第 1 课：能力协商
- 理解 initialize 阶段如何发现 Server 能力。
- 学习 capability-negotiation，知道 Host 为什么能列出工具、资源和 Prompt。

第 2 课：通知
- 学习 notification，理解不需要 result 的协议消息。
- 区分请求响应和单向事件通知。

第 3 课：sampling
- 学习 sampling，理解 Server 请求 Host 侧模型生成内容的场景。
- 重点关注权限边界和 Host 控制权。

第 4 课：elicitation
- 学习 elicitation，理解 Server 如何通过 Host 请求用户补充信息。
- 重点区分“Server 需要信息”和“Host 负责用户交互”。

第 5 课：roots
- 学习 roots，理解 Host 提供给 Server 的工作区边界。
- 思考为什么 Server 不应该默认拥有全盘访问范围。

第 6 课：authorization 和 security
- 学习授权、最小权限、用户确认和敏感数据保护。
- 思考 Tool 访问文件、网络或凭证前应该满足哪些条件。

第 7 课：tasks
- 学习长时间运行任务的设计思路。
- 区分一次性 Tool 调用和需要状态、进度、后续结果的任务。

第 8 课：调试闭环
- 调用 diagnose_issue 和 explain_error_message。
- 练习 get_practice_task("debug")。
- 按环境、启动命令、注册表、Host 重载、Client 调用顺序排查问题。
""",
}

__all__ = ["CURRICULUMS"]
