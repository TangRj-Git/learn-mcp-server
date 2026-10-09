# 官网对照改造与验收记录

> 本文是 2026-10-09 **前一阶段 FastMCP 3 / SDK 1 的历史快照**。之后已迁移主环境到 FastMCP 4.1.0 / SDK 2.3.0；当前状态与新版证据见 [检查与升级报告](../../reports/review-and-upgrade-2026-10-09.md)。下文“当前”“尚未迁移”等描述均指该阶段，原验收数据保留。

实施日期：2026-10-09。依据：[官网对照报告 G01–G34](../2026-10-08/official-docs-gap-analysis-2026-10-08.md)、[原审计 F01–F14](../2026-10-08/project-audit-2026-10-08.md)。原报告与 2026-10-08 证据保持为历史快照；本文记录改造后的实际状态。

## 改造结果与边界

G01–G29 的近期修复、完整教学闭环与工程改进已落实。G30、G31、G33 已提供带版本的概念/扩展专题。G34 已完成隔离源码兼容验证，主基线迁移尚未执行。报告明确列为可选的 G32 Elicitation 交互实验暂未实施。

主服务仍为 **20 Tools / 39 Resources / 5 Templates / 5 Prompts**，已有 MCP 名称和 URI/别名保留。教材包含 42 个概念、15 个代码示例主题和 14 个主题练习。独立 demo 展示实际三原语与结果，不增加主服务的注册规模。

主环境是 **FastMCP 3.4.8 / SDK 1.30.0 / Starlette 1.7.0 / Python 3.10.18 / 协议 2025-11-25**。主依赖分别限定 `<4`、`<2`，工作区锁定版本。FastMCP 4.1.0 / SDK 2.3.0 使用临时隔离环境；版本差异见 [版本说明](../../protocol-versions.md)。

调用链保留 `server → registry → tools/resources/prompts → data/utils`。新增的是完整教学实例、少量共用数据、输入校验和验证脚本。没有加入数据库、队列、动态插件扫描、LLM 判卷或自写协议层。

## G01–G34 状态映射

下表中的“已实现”同时对应源码与行为验证；“概念已覆盖”只指教材，不声称注册了可选协议能力。

| 编号 | 状态 | 具体改造 | 可核对的位置/结果 |
| --- | --- | --- | --- |
| G01 | 已实现 | 声明主基线，修正三原语、lifecycle、capabilities、roots、sampling、tasks | README、`data/concepts.py`、`data/references.py`、版本文档 |
| G02 | 已实现 | JSON 根/Server 对象、command/args/env/url 校验与传输冲突诊断 | `tools/config_tools.py`、`tests/test_regressions.py` |
| G03 | 已实现 | HTTP/HTTPS 主机与端口校验；拒绝凭证、fragment、非法字符；不联网 | `utils/validators.py`；合法/非法 URL 回归 |
| G04 | 已实现 | 本地 HTTP 开启框架 Host/Origin 防护 | `server.py`；外部 Origin 403、外部 Host 421、正常请求 200 |
| G05 | 已实现 | 三等级目标、操作与验收不同 | `data/curriculum.py`；不同计划及未知等级验证 |
| G06 | 已实现 | 关键词反馈显示检查点，明确不能证明答案正确 | `data/practices.py`、`tools/practice_tools.py`；错误/否定答案回归 |
| G07 | 已实现 | 补 tests 概念，学习衔接共用有效序列并有终点 | 概念、课程、练习；主题完整与终点验证 |
| G08 | 已实现 | 具体连接、import、stdout 证据优先于框架/传输名称 | `tools/debug_tools.py`；混合 stdio + ModuleNotFoundError 回归 |
| G09 | 已实现 | Prompt 空值、level、days 的业务校验与说明 | `prompts/learning_prompts.py`；1–30 及非法输入验证 |
| G10 | 已实现 | 更新主版本内依赖、锁文件与公告复核 | pyproject、uv.lock、下方依赖复核；真实传输与包验证 |
| G11 | 已实现 | 项目 version、instructions、Tool annotations、Resource/Prompt description | `server.py`、`registry.py`；发现元数据与初始化身份验证 |
| G12 | 已实现 | 包内单文件完整示例，工作区入口薄封装 | `demo.py`、`examples/minimal_server.py`；完整展示源码实际执行 |
| G13 | 已实现 | 必需参数、Field description、Literal enum、默认值示例 | `divide`；实际 inputSchema、非法 enum 验证 |
| G14 | 已实现 | 对象返回、outputSchema、content、structuredContent 的区别 | demo、学习指南；实际 value 与 Client data |
| G15 | 已实现 | 零分母、默认 ToolError、错误结果读取与未知工具行为 | `tests/test_demo.py`；按当前框架行为解释 |
| G16 | 已实现 | list/read 区分、JSON/Markdown MIME；v3 Template 小型适配 | `registry._markdown_template`；所有静态/模板实际读取 |
| G17 | 已实现 | Prompt 多消息、字符串 days 转换、参数限制 | demo、主 Prompt、`test_demo.py`；user/assistant 角色 |
| G18 | 已实现 | 内存 Client 串联发现、调用、静态/模板读取、Prompt | `examples/client_test.py`；主服务与 --demo 均通过 |
| G19 | 已实现 | 真实 stdio/HTTP Client，明确超时、cwd、本地端口和退出清理 | `examples/transport_client.py`、`tests/test_transports.py` |
| G20 | 已实现 | 旧协议请求、成功、协议错误、通知、工具业务错误示意 | 学习指南；明确简化字段、报文版本与观察方式 |
| G21 | 已实现 | 各原语与 schema/结构化结果/错误/tests 的专属练习 | 14 个主题任务；按检查点与实际结果验收 |
| G22 | 已实现 | Template 路径、可选 query、编码、未知值示例 | `demo://topics/{name}{?detail}`；编码/非法 bool/未知主题验证 |
| G23 | 已实现 | CurrentContext 注入，三个可观察进度事件 | `count_steps`；ctx 不在 schema，回调 1/2/3 |
| G24 | 已实现 | 有限超时、取消边界、连接退出后的清理验证 | `test_client_lifecycle.py`；不声称取消等于回滚 |
| G25 | 已实现 | 核心相邻概念同维度比较，支持反向顺序 | `CONCEPT_COMPARISONS`、`compare_concepts` |
| G26 | 已实现 | 正文单一数据源、官方出处与版本标签；demo 源码与教材共用 | `data/references.py`；42 个概念引用均有原目录中的 HTTP 200 抓取记录 |
| G27 | 已实现 | README、实际架构与学习文档分工，统一 Inspector 指引 | README、设计路线、学习指南；CLI 参数核对 |
| G28 | 已实现 | 函数/MCP/真实传输/安装包分层；Ruff、轻量 CI | 全部测试、CI、仓库外 wheel 结果 |
| G29 | 已实现 | factory 不再通过 globals 隐式导出所有功能 | `create_server()`；函数测试直导所属模块；外部 MCP 清单保留 |
| G30 | 概念已覆盖 | discovery、MRTR、listen、cache、扩展/弃用专题 | `data/concepts.py`、`protocol-versions.md`；标注新版 |
| G31 | 概念已覆盖 | Completion 是参数建议；cursor 不透明 | 概念与高级课程；未增加 handler/分页引擎 |
| G32 | 可选实验未实施 | 保留 Elicitation 能力前提与 accept/decline/cancel、安全边界讲解 | 需确定目标 Client/Host 后单独实验 |
| G33 | 概念已覆盖 | Apps / Skills / Tasks 扩展概览 | 概念、课程、官方扩展链接；未搭建扩展平台 |
| G34 | 隔离验证完成；主迁移未实施 | FastMCP 4.1.0 / SDK 2.3.0 副本测试与 modern 协商探针 | 158 tests / 8 warnings；依赖与教材切换仍见版本验收表 |

## 当前验证证据

本地执行证据是 Windows 的结果，不能替代 Ubuntu 或特定 Host 的实际验收。

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 锁文件 | `uv lock --check` 通过，87 个锁定包 | [check-01](implementation-2026-10-09/check-01.txt) |
| 已安装依赖兼容 | `uv pip check` 通过，检查 78 个包 | [check-02](implementation-2026-10-09/check-02.txt) |
| Ruff lint / format | 全部通过，46 个 Python 文件 | [check-03](implementation-2026-10-09/check-03.txt)、[check-04](implementation-2026-10-09/check-04.txt) |
| 全部测试 | **158 passed** | [pytest 输出](implementation-2026-10-09/check-05.txt) |
| 内存主 Client | 发现、调用、两类资源、Prompt 通过 | [check-06](implementation-2026-10-09/check-06.txt) |
| 内存 demo Client | 对象结果、JSON/Markdown、多消息、错误、进度通过 | [check-07](implementation-2026-10-09/check-07.txt) |
| 真实 stdio 脚本 | 通过，stdio 管道与子进程退出 | [check-08](implementation-2026-10-09/check-08.txt) |
| 真实 HTTP 脚本 | 临时本地端口调用通过，服务进程已清理 | [check-09](implementation-2026-10-09/check-09.txt) |
| 额外 mypy 2.4.0 | 30 个源码文件无问题；使用项目解释器、ignore-missing-imports | [验证汇总](implementation-2026-10-09/validation.json) |
| wheel / sdist | 构建通过 | [验证汇总](implementation-2026-10-09/validation.json) |
| 仓库外安装 wheel | 完整代码、学习 Resource、能力清单、demo 结果通过 | [wheel 结果](implementation-2026-10-09/wheel-smoke.json) |
| FastMCP 4 副本 | **158 passed, 8 warnings**；必要调整记录在版本文档 | [v4 测试](implementation-2026-10-09/fastmcp4-adapted-tests.txt)、[modern 探针](implementation-2026-10-09/fastmcp4-probe.json) |

CI 已加入 Windows/Ubuntu 的锁定安装、Ruff、真实传输、完整示例、构建与仓库外 wheel 验证。本次没有推送到远端触发 CI，不能据此宣称远端或 Ubuntu 检查已通过。mypy 使用临时工具核对，没有新增为项目运行依赖或 CI 的强制门禁。

### 安装包验证怎样避免仓库泄漏

使用单独 Python 3.10.19 虚拟环境，按主锁文件导出的运行依赖安装 wheel；切换到仓库外目录，并移除 PYTHONPATH。检查导入路径确实在独立环境的 `site-packages`，而不是项目的 `src/`。

验证脚本 [verify_installed_package.py](../../../scripts/verify_installed_package.py) 检查主能力数量、`get_code_example('minimal-server')`、`mcp://examples/minimal-server`、概念 Resource 与 demo 的 `divide`。CI 复用同一脚本。

本地复现（PowerShell，在项目根目录）：

```powershell
uv build
$taskWheelCheck = Join-Path $env:TEMP 'learn-mcp-wheel-check'
uv venv --python 3.10 $taskWheelCheck
uv pip install --python "$taskWheelCheck/Scripts/python.exe" -r docs/implementation-2026-10-09/runtime-requirements.txt dist/learn_mcp_server-0.1.0-py3-none-any.whl
```

随后在仓库外终端运行独立解释器与脚本的绝对路径，确保没有 PYTHONPATH 指向本仓库。脚本会拒绝直接从工作区导入的结果。

## 依赖公告复核

升级针对原审计的已知公告及其修复下限，保留当前主版本范围；下表是实际锁定版本，不是声称所有 future 版本都安全。

| 包 | 改造前 | 当前 | 原公告所列修复下限 |
| --- | --- | --- | --- |
| mcp | 1.27.2 | 1.30.0 | 1.28.1 |
| anyio | 4.13.0 | 4.15.1 | 4.14.2 |
| cryptography | 48.0.0 | 50.0.2 | 50.0.0（多项公告的最高下限） |
| pydantic-settings | 2.14.1 | 2.15.0 | 2.14.2 |
| python-multipart | 0.0.29 | 0.0.32 | 0.0.31 |
| Starlette | 1.2.1 | 1.7.0 | 1.3.1 |
| PyJWT | 2.13.0 | 2.15.1 | 已列修复项最高 2.15.0；此前另有未列 fix 的公告 |

本次从锁文件导出带 hash 的运行 requirements，在当前 Windows/Python 3.10 标记环境用 `pip-audit` 查询公告。结果为 **68 个审核条目、0 个已知漏洞、无 skip**。[原始 JSON](implementation-2026-10-09/dependency-audit.json)、[审核输入](implementation-2026-10-09/runtime-requirements.txt) 可复核。

“0 个已知漏洞”是该日、该版本、该数据库的查询结果，不等于数学上的无风险证明。原 PyJWT 未列 fix 项本次也没有被返回，准确结论是当前版本的扫描未检出，不能倒推每个公告都由项目代码修复。原环境的 pip/setuptools 公告也不再混入本次运行依赖清单。

没有凭依赖公告直接宣称当前静态学习 Server 可被利用；处理结果同时经过依赖兼容、真实传输和独立包安装验证。

## 兼容细节与后续工作

- 保留外部 MCP 注册名字与 URI。原先通过 `server.py` 隐式取普通函数的 Python 导入方式已调整，直接从所属 tools/resources/prompts 模块导入；项目内部调用与测试已更新。
- 主 Template 的 Markdown MIME 适配依据当前 3.4.8 实测。升级后再检查实际 contents，不只检查声明。
- 超时/取消不保证即刻停止或副作用回滚；当前生命周期测试验证退出内存 Client 后的 finally 清理。独立 HTTP 服务由其启动者关闭。
- FastMCP 4 副本的测试通过依赖临时测试调整和 `--no-deps` 的源码研究安装。正常依赖声明、教材、原生属性改写及新版专项测试尚未作为主项目迁移。
- G32 交互实验和 Apps/Skills/Tasks 实现仍是可选学习目标。主服务快查询没有增加任务队列或前端的需求。
- 本次未发布包、未创建提交/PR、未部署远程服务。构建产物位于被忽略的 `dist/`；改造与文档留在当前工作区供审阅。

阅读顺序：[README](../../../README.md) → [学习指南](../../learning-guide.md) → [当前架构](../../project-design-and-roadmap.md) → [版本与迁移](../../protocol-versions.md)。
