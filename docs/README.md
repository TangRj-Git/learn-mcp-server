# 文档目录

主课程基线：FastMCP 4.1.0 / SDK 2.3.0 / MCP 2026-07-28。首次使用从 [项目 README](../README.md) 开始。

## 当前指南

| 阅读顺序 | 文档 | 内容 |
| --- | --- | --- |
| 1 | [运行与配置](running-and-configuration.md) | 安装、主服务/demo、stdio/HTTP、Inspector、Host 配置 |
| 2 | [学习指南](learning-guide.md) | 按等级运行示例、观察协议结果并验收 |
| 3 | [项目架构](project-design-and-roadmap.md) | 文件职责、源码阅读顺序、修改入口与后续路线 |
| 4 | [版本说明](protocol-versions.md) | FastMCP/SDK/协议的区别、当前 API、历史握手与升级方法 |

示例文件说明在 [examples/README.md](../examples/README.md)，验证与打包脚本说明在 [scripts/README.md](../scripts/README.md)。

## 报告、证据与历史

| 目录 | 用途 | 入口 |
| --- | --- | --- |
| `reports/` | 最近完成的检查报告 | [详细检查与 FastMCP 4 升级](reports/review-and-upgrade-2026-10-09.md) |
| `evidence/` | 报告引用的版本查询、官方出处、运行与测试记录 | [证据说明](evidence/README.md) |
| `archive/` | 改造前审计、官网差距与 v3 阶段验收 | [历史记录索引](archive/README.md) |

报告中的版本、命令、测试数和路径反映其检查阶段。当前运行方式以指南为准；原始证据按日期保留，重新验证的输出写入被 Git 忽略的 `artifacts/`。

## 内容放置规则

- 启动和接入步骤放在运行指南；课程解释与验收放在学习指南。
- 模块职责和修改入口放在架构文档；版本/API 差异放在版本说明。
- 新检查报告放在 `reports/`，配套原始记录放在 `evidence/` 的日期目录。
- 过往报告连同其证据归入 `archive/`，保留原日期、事实和运行记录。
- 可继续复用的验收程序放在 `scripts/`；`examples/` 放学习者直接使用的示例。
