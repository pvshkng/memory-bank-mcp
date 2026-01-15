from fastmcp import Context
from fastmcp.server.dependencies import get_http_request

def get_user(ctx: Context) -> str | None:
    user = None
    if ctx.request_context:
        context = ctx.request_context
        user = context.request.query_params.get("user")        
    else:
        request = get_http_request()
        user = request.query_params.get("user")
    return user

