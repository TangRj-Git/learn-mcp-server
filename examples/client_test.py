import asyncio

from fastmcp import Client
from learn_mcp_server.server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
        prompts = await client.list_prompts()

        print("Tools:")
        for tool in tools:
            print(f"- {tool.name}")

        print("\nResources:")
        for resource in resources:
            print(f"- {resource.uri}")

        print("\nResource Templates:")
        for template in resource_templates:
            print(f"- {template.uriTemplate}")

        print("\nPrompts:")
        for prompt in prompts:
            print(f"- {prompt.name}")

        result = await client.call_tool("get_server_info", {})
        print("\nget_server_info result:")
        print(f"content blocks: {len(result.content)}")


if __name__ == "__main__":
    asyncio.run(main())
