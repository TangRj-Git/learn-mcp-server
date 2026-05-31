# 一、这个项目要做成什么样

这个项目可以叫：

```text
learn-mcp-server
```

它是一个使用 **FastMCP** 编写的本地 MCP Server，主要作用是帮助你学习 MCP 的核心概念、API 编写方式、传输方式、配置方式和调试方式。

它本身会暴露出：

```text
Tools
Resources
Resource Templates
Prompts
```

也就是说，你不仅会学习 MCP 的这些概念，还会在项目里面真实地把它们写出来。

---

# 二、这个 MCP 项目的定位

这个项目不是做业务系统，而是做一个：

```text
MCP 学习助手型 Server
```

它可以提供这些能力：

```text
1. 查询 MCP 概念
2. 查看 MCP 示例代码
3. 生成 MCP 学习计划
4. 解释 MCP 配置文件
5. 读取内置学习文档
6. 根据主题生成讲解 Prompt
7. 提供 Tool、Resource、Prompt 的真实示例
8. 支持 stdio 和 streamable-http 两种运行方式
9. 支持本地调试和后续接入 Claude Code、Codex、MCP Inspector 等工具
```

---

# 三、项目整体功能设计

这个学习 MCP 的 MCP，可以分成 6 个核心模块。

---

## 1. 基础信息模块

这个模块用来让用户了解这个 MCP Server 是什么、能做什么、包含哪些功能。

主要功能包括：

```text
get_server_info
list_learning_modules
get_learning_path
```

示例效果：

```text
用户问：这个 MCP Server 能做什么

模型可以调用 get_server_info 工具，然后返回这个学习 MCP Server 的介绍。
```

---

## 2. MCP 概念学习模块

这个模块用来讲解 MCP 的核心概念。

包含内容：

```text
MCP 是什么
Host 是什么
Client 是什么
Server 是什么
Tool 是什么
Resource 是什么
Prompt 是什么
Transport 是什么
stdio 是什么
SSE 是什么
Streamable HTTP 是什么
JSON-RPC 是什么
生命周期是什么
能力协商是什么
通知是什么
采样是什么
根目录是什么
Elicitation 是什么
Authorization 是什么
Security 安全边界是什么
Tasks 长时间运行任务是什么
```

对应可以设计成 Tool：

```text
explain_concept(concept: str)
compare_concepts(left: str, right: str)
get_concept_map()
```

也可以设计成 Resource：

```text
mcp://docs/concepts
mcp://docs/host-client-server
mcp://docs/tools
mcp://docs/resources
mcp://docs/prompts
mcp://docs/transports
```

---

## 3. MCP API 示例模块

这个模块是项目最重要的部分之一。

它用来展示 FastMCP 里面常见 API 的写法。

包含：

```text
Tool 示例
Resource 示例
Resource Template 示例
Prompt 示例
参数类型示例
返回值示例
异常处理示例
同步函数示例
异步函数示例
带 docstring 的示例
带装饰器参数的示例
```

可以设计这些 Resource：

```text
mcp://examples/tool-basic
mcp://examples/tool-params
mcp://examples/resource-basic
mcp://examples/resource-template
mcp://examples/prompt-basic
mcp://examples/async-tool
mcp://examples/error-handling
mcp://examples/end-to-end-client
```

也可以设计这些 Tool：

```text
get_code_example(topic: str)
list_code_examples()
explain_code_example(example_name: str)
```

---

## 4. MCP 配置学习模块

这个模块专门讲解 MCP 怎么被 Host 使用。

比如：

```text
Claude Code 里面怎么配置本地 stdio MCP
Codex 里面怎么配置本地 MCP
为什么 command 推荐使用 uvx 或 uv
为什么 args 里面有 --from、包名和版本号
uvx 和 npx 这类临时运行工具有什么相似点
stdio 配置是什么
streamable-http 配置是什么
本地配置和远程配置有什么区别
```

可以设计 Tool：

```text
explain_config(config_text: str)
generate_stdio_config(command: str, args: list[str])
generate_http_config(server_url: str)
compare_local_and_remote_config()
```

可以设计 Resource：

```text
mcp://docs/config-stdio
mcp://docs/config-http
mcp://docs/config-local-vs-remote
mcp://docs/config-common-errors
```

---

## 5. 学习任务与练习模块

这个模块用来让这个 MCP 不只是“看文档”，还可以“带你练”。

可以包含：

```text
生成学习路线
生成今日学习任务
生成练习题
检查答案
推荐下一步学习内容
```

可以设计 Tool：

```text
generate_learning_plan(level: str)
get_practice_task(topic: str)
check_answer(topic: str, answer: str)
suggest_next_step(current_topic: str)
```

示例：

```text
用户问：我已经学完 Tool 了，下一步学什么

模型可以调用 suggest_next_step，返回 Resource、Prompt、Transport 的学习顺序。
```

---

## 6. 调试与诊断模块

这个模块用于帮助你排查 MCP 项目常见问题。

比如：

```text
服务启动了但是工具看不到
stdio 没有输出
HTTP 端点访问失败
配置文件路径写错
Python 虚拟环境问题
函数 docstring 缺失
参数类型不清晰
返回值不能序列化
装饰器写错
Host 没有重新加载 MCP
```

可以设计 Tool：

```text
diagnose_issue(issue_description: str)
list_common_errors()
explain_error_message(error_text: str)
```

可以设计 Resource：

```text
mcp://debug/common-errors
mcp://debug/stdio-errors
mcp://debug/http-errors
mcp://debug/config-errors
```

---

# 四、项目目录结构设计

后面我们会真正创建这个目录。现在先看结构。

```text
learn-mcp-server/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── learn_mcp_server/
│       │
│       ├── __init__.py
│       ├── server.py
│       ├── registry.py
│       ├── settings.py
│       │
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── basic_tools.py
│       │   ├── concept_tools.py
│       │   ├── example_tools.py
│       │   ├── config_tools.py
│       │   ├── practice_tools.py
│       │   └── debug_tools.py
│       │
│       ├── resources/
│       │   ├── __init__.py
│       │   ├── concept_resources.py
│       │   ├── example_resources.py
│       │   ├── config_resources.py
│       │   ├── curriculum_resources.py
│       │   └── debug_resources.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── learning_prompts.py
│       │
│       ├── data/
│       │   ├── concepts.py
│       │   ├── examples.py
│       │   ├── curriculum.py
│       │   ├── configs.py
│       │   └── practices.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── formatters.py
│           └── validators.py
│
├── tests/
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_prompts.py
│   ├── test_examples.py
│   ├── test_structure.py
│   └── test_mcp_integration.py
│
└── examples/
    ├── stdio_config.json
    ├── streamable_http_config.json
    └── client_test.py
```

---

# 五、每个目录的作用

## 1. `server.py`

这是 MCP Server 的入口文件。

主要负责：

```text
创建 FastMCP 实例
注册 Tool
注册 Resource
注册 Prompt
选择运行方式
启动 MCP Server
```

它是整个项目的核心入口。

---

## 2. `tools/`

这个目录专门放 MCP Tools。

Tool 的特点是：

```text
模型可以主动调用
适合执行动作
适合计算
适合生成结果
适合处理用户输入
```

例如：

```text
解释一个 MCP 概念
生成一个学习计划
分析一段配置
诊断一个错误
生成一个练习题
```

---

## 3. `resources/`

这个目录专门放 MCP Resources。

Resource 的特点是：

```text
提供可读取的上下文
更像文档、资料、说明书
通常通过 URI 访问
不强调执行动作
```

例如：

```text
mcp://docs/tools
mcp://docs/resources
mcp://examples/basic-tool
mcp://debug/common-errors
```

---

## 4. `prompts/`

这个目录专门放 MCP Prompts。

Prompt 的特点是：

```text
提供可复用的提示词模板
帮助模型按照固定方式完成任务
适合教学、总结、解释、代码生成
```

例如：

```text
生成 MCP 学习总结
讲解某个 MCP 概念
根据用户水平生成学习路线
分析 MCP 代码
```

---

## 5. `data/`

这个目录存放项目内置数据。

比如：

```text
MCP 概念说明
示例代码文本
配置模板
练习题
常见错误说明
```

这样做的好处是：
Tool、Resource、Prompt 的逻辑不会和大量文本内容混在一起。

---

## 6. `utils/`

这个目录放通用辅助函数。

例如：

```text
格式化返回内容
检查参数是否合法
把列表转成 Markdown
把错误信息整理成结构化内容
```

---

## 7. `tests/`

这个目录放测试代码。

后面可以测试：

```text
Tool 是否正常返回
Resource 是否能读取
Prompt 是否能生成
配置解析是否正常
异常处理是否符合预期
```

---

## 8. `examples/`

这个目录放使用示例。

例如：

```text
stdio 配置示例
streamable-http 配置示例
客户端调用示例
调试脚本
```

---

# 六、这个项目最终会包含哪些 MCP 能力

最终这个项目会覆盖 MCP 学习中非常重要的几个点。

```text
1. FastMCP Server 创建
2. Tool 编写
3. Resource 编写
4. Resource Template 编写
5. Prompt 编写
6. stdio 运行
7. streamable-http 运行
8. 本地配置
9. 远程配置思路
10. MCP Inspector 调试
11. Claude Code 接入
12. Codex 接入
13. 常见错误排查
14. 项目拆分和模块化
15. 测试
16. 打包
17. 发布
```

---

# 七、项目功能清单初版

下面是这个项目第一版可以实现的功能。

## Tools

```text
get_server_info()
list_learning_modules()
get_learning_path()
explain_concept(concept: str)
compare_concepts(left: str, right: str)
get_concept_map()
list_code_examples()
get_code_example(topic: str)
explain_code_example(example_name: str)
generate_learning_plan(level: str)
get_practice_task(topic: str)
check_answer(topic: str, answer: str)
suggest_next_step(current_topic: str)
explain_config(config_text: str)
generate_stdio_config(command: str, args: list[str])
generate_http_config(server_url: str)
compare_local_and_remote_config()
diagnose_issue(issue_description: str)
explain_error_message(error_text: str)
list_common_errors()
```

---

## Resources

```text
mcp://docs/introduction
mcp://docs/concepts
mcp://docs/architecture
mcp://docs/host-client-server
mcp://docs/tools
mcp://docs/resources
mcp://docs/resource-template
mcp://docs/prompts
mcp://docs/transports
mcp://docs/stdio
mcp://docs/streamable-http
mcp://docs/json-rpc
mcp://docs/lifecycle
mcp://docs/elicitation
mcp://docs/authorization
mcp://docs/security
mcp://docs/tasks
mcp://docs/config-stdio
mcp://docs/config-http
mcp://docs/config-local-vs-remote
mcp://docs/config-common-errors
mcp://curriculum/beginner
mcp://curriculum/intermediate
mcp://curriculum/advanced
mcp://examples/basic-tool
mcp://examples/basic-resource
mcp://examples/tool-basic
mcp://examples/resource-basic
mcp://examples/resource-template
mcp://examples/basic-prompt
mcp://examples/prompt-basic
mcp://examples/tool-params
mcp://examples/async-tool
mcp://examples/error-handling
mcp://examples/end-to-end-client
mcp://debug/common-errors
mcp://debug/stdio-errors
mcp://debug/http-errors
mcp://debug/config-errors
```

---

## Resource Templates

```text
mcp://concepts/{name}
mcp://examples/{name}
mcp://configs/{name}
mcp://debug/{error_type}
mcp://curriculum/{level}
```

Resource Template 的作用是根据参数动态返回资源内容。

例如：

```text
mcp://concepts/tool
mcp://concepts/resource
mcp://examples/basic-tool
mcp://debug/stdio
mcp://curriculum/beginner
```

---

## Prompts

```text
explain_mcp_topic(topic: str, level: str)
generate_mcp_study_plan(level: str, days: int)
review_mcp_code(code: str)
debug_mcp_error(error: str)
summarize_mcp_concept(topic: str)
```

---

# 八、建议的开发顺序

这个项目不要一口气写完，建议按照下面顺序来。

---

## 第 1 阶段：项目初始化

目标：

```text
创建项目目录
创建虚拟环境
安装依赖
创建基础文件
写最小可运行 FastMCP Server
使用 stdio 启动
```

这一阶段只需要实现一个最简单的工具：

```text
get_server_info()
```

只要这个工具能被看到、能被调用，就说明项目基础打通了。

---

## 第 2 阶段：实现基础 Tool

目标：

```text
实现 get_server_info
实现 list_learning_modules
实现 explain_concept
实现 compare_concepts
```

这一阶段主要学习 Tool 怎么写。

重点掌握：

```text
@mcp.tool()
函数名
函数参数
函数返回值
docstring
参数类型注解
异常处理
```

---

## 第 3 阶段：实现 Resource

目标：

```text
实现 mcp://docs/introduction
实现 mcp://docs/tools
实现 mcp://docs/resources
实现 mcp://docs/prompts
实现 mcp://docs/transports
```

这一阶段主要学习 Resource 怎么写。

重点掌握：

```text
@mcp.resource()
URI 命名
静态资源
资源返回值
Resource 和 Tool 的区别
```

---

## 第 4 阶段：实现 Resource Template

目标：

```text
实现 mcp://concepts/{name}
实现 mcp://examples/{name}
实现 mcp://debug/{error_type}
```

这一阶段主要学习动态资源。

重点掌握：

```text
固定 Resource
动态 Resource Template
URI 参数
路径变量
资源内容动态生成
```

---

## 第 5 阶段：实现 Prompt

目标：

```text
实现 explain_mcp_topic
实现 generate_mcp_study_plan
实现 review_mcp_code
实现 debug_mcp_error
```

这一阶段主要学习 Prompt 的写法。

重点掌握：

```text
@mcp.prompt()
Prompt 函数
Prompt 参数
Prompt 返回文本
Prompt 和 Tool 的区别
Prompt 适合什么场景
```

---

## 第 6 阶段：模块化拆分

目标：

```text
把 server.py 里面的代码拆分出去
tools 放 tools 目录
resources 放 resources 目录
prompts 放 prompts 目录
数据放 data 目录
```

这一阶段主要学习 MCP 项目的工程化结构。

---

## 第 7 阶段：增加 streamable-http 运行方式

目标：

```text
支持 stdio 运行
支持 streamable-http 运行
支持通过配置切换 transport
```

这一阶段主要学习 MCP 的传输方式。

---

## 第 8 阶段：接入外部 Host

目标：

```text
生成本地 stdio 配置
配置到 Claude Code
配置到 Codex
查看工具列表
调用工具
读取资源
使用 Prompt
```

这一阶段主要学习 MCP Server 怎么被 Host 使用。

---

## 第 9 阶段：测试

目标：

```text
测试工具函数
测试资源函数
测试 Prompt 函数
测试配置解析
测试异常情况
```

这一阶段主要保证项目后续扩展不容易坏。

---

## 第 10 阶段：打包与发布

目标：

```text
整理 pyproject.toml
整理 README.md
添加命令行入口
添加版本号
本地安装测试
发布前检查
```

这一阶段主要把项目变成一个真正可复用的 MCP 项目。

---

# 九、第一版项目不要做得太复杂

第一版建议只做这些：

```text
1. 一个 server.py
2. 一个 get_server_info 工具
3. 一个 explain_concept 工具
4. 一个 mcp://docs/introduction 资源
5. 一个 explain_mcp_topic prompt
6. 使用 stdio 启动
```

第一版跑通之后，再开始拆模块。

不要一开始就写很多目录和很多文件，否则容易出现：

```text
导入路径错误
虚拟环境错误
配置路径错误
Host 找不到 server
模块拆分之后注册失败
工具看不到
资源读不到
```

学习型项目最重要的是先跑通，再变复杂。

---

# 十、完整大纲

下面是后续我会带你一步一步完成的完整路线。

```text
第 0 步：明确项目目标和最终效果

第 1 步：创建项目目录
第 2 步：创建 Python 虚拟环境
第 3 步：安装 FastMCP 相关依赖
第 4 步：创建最小 server.py
第 5 步：写第一个 Tool
第 6 步：使用 stdio 启动 MCP Server
第 7 步：用调试工具查看这个 MCP Server

第 8 步：增加多个 Tool
第 9 步：讲解 Tool 的函数名、参数、返回值、docstring
第 10 步：增加 MCP 概念查询功能
第 11 步：增加代码示例查询功能
第 12 步：增加配置解释功能

第 13 步：增加第一个 Resource
第 14 步：讲解 Resource URI 的设计
第 15 步：增加多个文档 Resource
第 16 步：增加 Resource Template
第 17 步：讲解 Resource 和 Resource Template 的区别

第 18 步：增加第一个 Prompt
第 19 步：讲解 Prompt 的适用场景
第 20 步：增加学习计划 Prompt
第 21 步：增加代码审查 Prompt
第 22 步：增加错误诊断 Prompt

第 23 步：重构项目结构
第 24 步：拆分 tools 模块
第 25 步：拆分 resources 模块
第 26 步：拆分 prompts 模块
第 27 步：拆分 data 模块
第 28 步：解决模块导入和注册问题

第 29 步：支持 stdio transport
第 30 步：支持 streamable-http transport
第 31 步：讲解两种 transport 的区别
第 32 步：讲解什么时候需要自己启动 Server
第 33 步：讲解什么时候由 Host 启动 Server

第 34 步：编写本地 MCP 配置
第 35 步：接入 Claude Code
第 36 步：接入 Codex
第 37 步：查看工具列表
第 38 步：调用工具
第 39 步：读取资源
第 40 步：使用 Prompt

第 41 步：增加错误诊断模块
第 42 步：增加常见错误 Resource
第 43 步：增加配置解释 Tool
第 44 步：增加学习任务 Tool
第 45 步：增加答案检查 Tool

第 46 步：添加测试目录
第 47 步：测试 Tool 函数
第 48 步：测试 Resource 函数
第 49 步：测试 Prompt 函数
第 50 步：测试异常情况

第 51 步：整理 README
第 52 步：整理 pyproject.toml
第 53 步：添加命令行入口
第 54 步：本地安装运行
第 55 步：准备发布
```

---

# 十一、最终项目效果

完成之后，你会得到一个完整的 MCP 学习项目。

它既是一个 MCP Server，又是一个 MCP 教学案例。

你可以通过它学会：

```text
MCP Server 怎么写
FastMCP 怎么用
Tool 怎么写
Resource 怎么写
Prompt 怎么写
Resource Template 怎么写
stdio 怎么运行
streamable-http 怎么运行
MCP 配置怎么写
Host 怎么发现工具
模型怎么调用工具
项目怎么模块化
MCP 项目怎么测试
MCP 项目怎么发布
```

---

# 十二、当前可运行版本

当前项目已经实现第一版 MCP 学习 Server。

## 已实现能力

```text
Tools: 20 个
Resources: 39 个
Resource Templates: 5 个
Prompts: 5 个
```

## 当前代码结构

```text
server.py：只负责创建 FastMCP 实例、调用 registry.register_all、提供 main 入口
registry.py：集中维护 Tools/Resources/Prompts 的注册清单，并把 FastMCP 实例作为依赖传入
data/：存放概念、示例、配置、练习等内置数据
tools/：存放 Tool 函数实现
resources/：存放静态 Resource 和 Resource Template 函数实现
curriculum_resources.py：提供 beginner/intermediate/advanced 三条学习课程资源
prompts/：存放 Prompt 模板函数实现
tests/：覆盖函数级测试、结构测试和 FastMCP Client 集成测试
```

## 给别人使用的 stdio 配置

发布到 PyPI 后，推荐让 Host 使用 `uvx` 启动：

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

这种方式不需要用户手动创建虚拟环境，也不需要配置本机 Python 解释器路径。

## 本地开发 stdio 配置

如果还没有发布包，或者想在当前工作区调试，可以让 Host 使用 `uv run --directory`：

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

## 使用 uv 环境运行测试

```powershell
uv sync
uv run pytest -q
```

当前测试覆盖包括：

```text
Tool 函数测试
Resource 函数测试
Prompt 函数测试
示例配置测试
模块结构测试
FastMCP Client 集成测试
```

## 使用 Inspector 调试

```powershell
cd E:\SoftwareProject\learn-mcp-server
uv run fastmcp dev inspector src\learn_mcp_server\server.py
```

## 本地客户端测试

```powershell
cd E:\SoftwareProject\learn-mcp-server
uv run python examples\client_test.py
```

## streamable-http 运行方式

```powershell
$env:LEARN_MCP_TRANSPORT="streamable-http"
uv run learn-mcp-server
```

默认地址：

```text
http://127.0.0.1:8000/mcp
```

---
