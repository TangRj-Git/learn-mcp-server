CONFIG_DOCS = {
    "stdio": """
# stdio 配置

这里展示生态常见 mcpServers JSON；具体 Host 可能用其他格式，需查产品官方文档。

stdio 配置适合本地 MCP Server。Host 会启动一个本地进程，并通过标准输入输出交换 MCP 消息。

发布后推荐使用 uvx 运行。uvx 会为这个 MCP Server 创建隔离环境并自动安装依赖，不需要用户手动配置 Python 解释器路径。

发布版示例：

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "learn-mcp-server==0.2.0",
        "learn-mcp-server"
      ]
    }
  }
}
```

本地开发示例（替换为自己的项目绝对路径，Host 需要能找到 uv）：

```json
{
  "mcpServers": {
    "learn-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "--locked",
        "--directory",
        "E:/SoftwareProject/learn-mcp-server",
        "learn-mcp-server"
      ],
      "env": {
        "LEARN_MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```
""",
    "streamable-http": """
# streamable-http 配置

这是生态常见 mcpServers JSON，不保证适用于全部 Host。

streamable-http 配置适合已经通过 HTTP 运行的 MCP Server。

示例：

```json
{
  "mcpServers": {
    "learn-mcp-server-http": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```
""",
    "local-vs-remote": """
# 本地配置和远程配置

本地 stdio 配置通常包含 command 和 args，由 Host 负责启动进程。

给别人使用时，推荐 command 使用 uvx，并通过 --from 指定包名和版本。

本地开发时，推荐 command 使用 uv，并通过 run --directory 指向项目目录。

远程或 HTTP 配置通常包含 url，由 Host 连接已经运行的 MCP 服务。
""",
    "common-errors": """
# 配置常见错误

常见配置问题包括：

1. 启动命令不可执行、PATH 不正确或解释器环境不匹配
2. uvx 的 --from 包名或版本号写错
3. 本地开发配置中的 uv run --directory 路径写错
4. stdio 配置中误写了 url
5. streamable-http 配置中服务没有启动
6. 修改配置后没有重启 Host
""",
}

DEBUG_GUIDES = {
    "stdio": """
# stdio 调试

stdio 模式通过标准输入和标准输出传输 MCP 协议消息。

调试时要注意：

1. 不要使用 print 输出普通日志
2. stdout 是协议通道
3. 普通日志应写入 stderr 或日志文件
4. Host 修改配置后通常需要重启
""",
    "stdio-errors": """
# stdio 错误

stdio 常见错误包括：

1. 使用 print 污染 stdout 协议通道
2. command 无法执行；Python/Node/二进制均可用，uv 是推荐而非必需
3. uvx 的 --from 包名或版本号不正确
4. 本地开发配置中的 uv run --directory 路径不正确
""",
    "http-errors": """
# HTTP 错误

streamable-http 常见错误包括：

1. MCP Server 没有启动
2. url 与实际 endpoint 不符，本项目默认 /mcp
3. 端口被占用
4. Host 无法访问对应地址
5. 无效 Origin 返回 403，不可信 Host 返回 421
6. CORS、Origin 防护与身份授权是不同机制
""",
    "config-errors": """
# 配置错误

配置常见错误包括：

1. JSON 格式不合法
2. mcpServers 字段缺失
3. stdio 的 command 或 args 写错
4. streamable-http 的 url 写错
""",
    "common-errors": """
# 常见错误

常见 MCP 调试问题包括：

1. 启动命令不可执行，或使用 uv/uvx 时未安装 uv、包名/版本无法解析
2. 启动命令路径写错
3. 本地开发配置中的 --directory 不在期望目录
4. 工具函数缺少类型注解
5. Resource URI 写错
""",
}

__all__ = ["CONFIG_DOCS", "DEBUG_GUIDES"]
