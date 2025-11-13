from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool
def greet(name: str) -> str:
    """Greet someone"""
    return f"Hello, {name}!"


@mcp.tool
def process_data(input: str) -> str:
    """Process some data"""
    return f"Processed: {input}"

app = mcp.http_app()
