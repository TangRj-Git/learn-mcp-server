# 维护脚本

这里放项目验收程序。学习用 Client 和 Server 入口在 [examples/](../examples/README.md)。

| 脚本 | 使用条件 | 验证内容 |
| --- | --- | --- |
| [verify_runtime.py](verify_runtime.py) | 已执行 uv sync，默认从源码工作区复验 | 主服务内存/stdio/HTTP 的三种模式，demo auto/legacy，共 11 组 Client；4 组原始现代 HTTP |
| [verify_installed_package.py](verify_installed_package.py) | 仓库外工作目录 + 独立环境，安装构建出的 wheel | 包来源、三原语、包内示例、MIME、demo 与安装包 stdio 子进程 |

## 复验运行

```powershell
uv run --locked python scripts/verify_runtime.py
```

结果默认写入 `artifacts/runtime/`：Client JSON、原始 HTTP 报文与临时 Server 日志。该目录已被 Git 忽略；历史报告引用的文件继续保存在 `docs/evidence/`。可用 `--output-dir` 指定另一个输出目录。

脚本有导入保护，不会在被导入时运行；HTTP 子进程在 finally 中清理。检查失败时保留输出和异常，不能把失败视为通过。

## 验收安装包

先在项目根目录运行 `uv build`。然后创建仓库外虚拟环境、导出非开发的固定依赖、正常安装 wheel，并在仓库外运行：

```text
<独立环境的 Python> <项目绝对路径>/scripts/verify_installed_package.py
```

不要用 `uv run` 从源码工作区执行该脚本来代替安装验收。它要求从独立环境的 site-packages 导入项目，并检查包内完整示例不依赖仓库相对路径。[CI 的 Verify wheel outside checkout 步骤](../.github/workflows/ci.yml) 提供完整创建、安装与执行流程。

## 常规检查

```powershell
uv run --locked ruff check src tests examples scripts
uv run --locked ruff format --check src tests examples scripts
uv run --locked pytest -o addopts=""
uv pip check
uv build
```

pytest 已将 FastMCP 兼容弃用警告按错误处理；CI 另设置 `FASTMCP_MCP_CAMELCASE_COMPAT=false`。具体检查范围见 [项目架构](../docs/project-design-and-roadmap.md)。
