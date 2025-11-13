from fastmcp import FastMCP, Context
from pydantic import Field
from lib.redis import get_redis_client, get_memory_key
from lib.helper import get_user
from datetime import datetime

mcp = FastMCP(name="Memory Bank MCP Server")


@mcp.tool(name="memory.remember")
async def remember(
    ctx: Context,
    record: str = Field(
        ...,
        description=""" Details of the memory item to store such as user's preferences, history, and key details.""",
    ),
) -> str:
    """Store a memory item about a user's preferences, history, and key details across multiple sessions."""

    user = get_user(ctx)
    if not user:
        return "Memory feature is not available for guest users."

    client = get_redis_client()
    key = get_memory_key(user)

    try:
        exist = client.exists(key)
        if exist:
            client.json.arrappend(key, "$", record)
        else:
            client.json.set(key, "$", [record])

    except Exception as e:
        return f"Error storing memory item: {str(e)}"
    return f"Stored memory about: {record} on {datetime.utcnow().isoformat()} UTC"


@mcp.tool(name="memory.forget")
async def forget(
    ctx: Context,
    index: int = Field(..., description=""" Index of the memory item to remove."""),
) -> str:
    """Remove a memory item by its index."""

    user = get_user(ctx)
    if not user:
        return "Memory feature is not available for guest users."

    client = get_redis_client()
    key = get_memory_key(user)
    try:
        result = client.json.arrpop(key, "$", index)
        if result:
            return f"Removed memory item at index {index} about : {result[0]}"
        else:
            return f"No memory item found at index {index}."

    except Exception as e:
        return f"Error removing memory item {index}: {str(e)}"


@mcp.resource("resource://memory.recall")
async def recall(ctx: Context) -> dict:
    user = get_user(ctx)
    if not user:
        return {"error": "User not found"}
    try:
        client = get_redis_client()
        key = get_memory_key(user)
        memory = client.json.get(key, "$")
        return memory[0] if memory else []

    except Exception as e:
        return {"error": str(e)}


app = mcp.http_app(stateless_http=True, transport="streamable-http")
