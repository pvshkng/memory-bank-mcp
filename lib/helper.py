from fastmcp import Context
from starlette.requests import Request

def get_user(ctx: Context) -> str:
    req: Request = ctx.get_http_request()
    user = req.headers.get("x-user-email")
    return user