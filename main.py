from fastmcp import FastMCP, Context
from starlette.requests import Request
from typing import List, Annotated, Optional
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
def forget(
    ctx: Context, key: str, value: str = Field(..., description=""" Details """)
) -> str:
    """Remove a memory item about a user from the memory bank."""
    return f"Stored memory item with key: {key}"


@mcp.resource("resource://memory.recall")
async def recall(ctx: Context) -> dict:
    user = get_user(ctx)
    if not user:
        return {"error": "User not found"}
    client = get_redis_client()
    key = get_memory_key(user)
    memory = client.json.get(key, "$")
    return {"memory": memory}


@mcp.tool
def greet(name: str) -> str:
    """Greet someone"""
    return f"Hello, {name}!"


@mcp.tool
def process_data(input: str) -> str:
    """Process some data"""
    return f"Processed: {input}"


app = mcp.http_app(stateless_http=True, transport="streamable-http")
