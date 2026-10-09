# 检查证据

[upgrade-2026-10-09/](upgrade-2026-10-09) 对应 [FastMCP 4 检查与升级报告](../reports/review-and-upgrade-2026-10-09.md)。该目录保存升级阶段的原始事实，复验时不覆盖这些文件。

| 查找内容 | 文件 |
| --- | --- |
| 版本与运行环境 | [FastMCP 元数据](upgrade-2026-10-09/fastmcp-metadata.json)、[SDK 元数据](upgrade-2026-10-09/mcp-metadata.json)、[环境记录](upgrade-2026-10-09/environment.json) |
| 官方依据 | [来源清单](upgrade-2026-10-09/official-sources.json)、[原文摘录](upgrade-2026-10-09/official-excerpts.md) |
| 测试与静态检查 | [pytest](upgrade-2026-10-09/pytest.txt)、[Ruff](upgrade-2026-10-09/ruff-check.txt)、[Mypy](upgrade-2026-10-09/mypy.txt) |
| Client 与原始 HTTP | [Client 输出](upgrade-2026-10-09/cli-runtime.json)、[wire 报文](upgrade-2026-10-09/modern-wire.json) |
| 构建与仓库外安装 | [构建日志](upgrade-2026-10-09/build.txt)、[安装及验收日志](upgrade-2026-10-09/wheel-install-and-check.txt) |
| 依赖已知漏洞审计 | [runtime 导出](upgrade-2026-10-09/runtime-requirements.txt)、[审计结果](upgrade-2026-10-09/pip-audit-runtime.json) |

日志、JSON 和 `runtime-probe.py` 中的原始路径/脚本均是当时的快照。目录移动后应通过 [scripts/verify_runtime.py](../../scripts/verify_runtime.py) 复跑，其新输出写入 `artifacts/runtime/`，保持历史依据可追溯。
