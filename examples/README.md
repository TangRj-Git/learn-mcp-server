# 学习示例

从项目根目录通过 `uv run --locked python ...` 执行。完整安装和接入步骤见 [运行与配置](../docs/running-and-configuration.md)。

| 文件 | 连接/启动什么 | 适合观察什么 |
| --- | --- | --- |
| [client_test.py](client_test.py) | 默认主服务内存连接；`--demo` 选择教学实例 | 能力发现、Tool 结果、Resource/Template MIME、Prompt、demo 进度与错误 |
| [transport_client.py](transport_client.py) | 主服务 stdio 子进程或已经运行的 HTTP 服务 | 真实进程和 HTTP 传输、超时与连接清理 |
| [minimal_server.py](minimal_server.py) | 导入并启动包内 demo | stdio/Inspector 入口；完整实现只有一份，在 [demo.py](../src/learn_mcp_server/demo.py) |
| [workspace_stdio_config.json](workspace_stdio_config.json) | Host 启动当前源码工作区 | 推荐的本地接入方式，无须发布安装包 |
| [streamable_http_config.json](streamable_http_config.json) | Host 连接本地 HTTP 主服务 | 先启动服务，再按 URL 接入 |
| [stdio_config.json](stdio_config.json) | Host 通过 uvx 启动已发布包 | 发布后的配置示意，不能代替当前工作区配置 |

常用顺序：

```powershell
uv run --locked python examples/client_test.py
uv run --locked python examples/client_test.py --demo
uv run --locked python examples/transport_client.py stdio
```

`mcp://...` 资料属于主服务，`divide` 与 `demo://...` 属于 demo。两个 Client 都接受 `--mode auto`、`--mode 2026-07-28`、`--mode legacy`。`client_test.py` 是演示命令，pytest 的测试集中在 `tests/`。

安装包验收和批量运行验证已归入 [scripts/](../scripts/README.md)。
