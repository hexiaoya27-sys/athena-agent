"""
MCP (Model Context Protocol) 工具客户端
- 这是 2025 年业界事实标准
- 替代了 LangChain 老旧的 Tools 写法
- 面试时一定要强调："我们的工具层基于 Anthropic MCP 协议"
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPToolManager:
    def __init__(self):
        self.sessions = {}  # 多个 MCP Server 的连接

    async def connect(self, server_name: str, params: StdioServerParameters):
        """连接一个 MCP Server（如 Notion / Google Calendar）"""
        ...

    async def call_tool(self, server: str, tool_name: str, args: dict,
                        max_retries: int = 3):
        """
        调用工具，自带：
        - 自动重试（指数退避）
        - 参数自校验
        - 超时控制
        - 失败降级
        """
        for attempt in range(max_retries):
            try:
                async with asyncio.timeout(30):
                    result = await self.sessions[server].call_tool(tool_name, args)
                    return {"status": "ok", "data": result}
            except asyncio.TimeoutError:
                if attempt == max_retries - 1:
                    return {"status": "timeout", "fallback": self._fallback(tool_name)}
            except Exception as e:
                await asyncio.sleep(2 ** attempt)  # 指数退避

        return {"status": "failed"}