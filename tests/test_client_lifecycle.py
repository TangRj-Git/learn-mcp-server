"""等待失败与连接清理分开验证；取消不会回滚业务副作用。"""

import asyncio

import pytest
from fastmcp import Client, FastMCP
from mcp.shared.exceptions import MCPError
from mcp_types import REQUEST_TIMEOUT


@pytest.mark.parametrize("action", ["timeout", "cancel"])
def test_client_wait_failure_still_cleans_up_on_context_exit(action):
    async def check():
        started = asyncio.Event()
        cleaned_up = asyncio.Event()
        server = FastMCP("client-lifecycle-test")

        @server.tool()
        async def wait_for_exit() -> str:
            try:
                started.set()
                await asyncio.Event().wait()
                return "finished"
            finally:
                cleaned_up.set()

        async with Client(server, timeout=0.2 if action == "timeout" else 10) as client:
            request = asyncio.create_task(client.call_tool("wait_for_exit", {}))
            await asyncio.wait_for(started.wait(), timeout=2)
            if action == "cancel":
                request.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await request
            else:
                with pytest.raises(MCPError) as error:
                    await asyncio.wait_for(request, timeout=2)
                assert error.value.code == REQUEST_TIMEOUT

        # 只断言退出连接后的清理，不把超时当作立即停止或事务回滚的保证。
        await asyncio.wait_for(cleaned_up.wait(), timeout=2)

    asyncio.run(check())
