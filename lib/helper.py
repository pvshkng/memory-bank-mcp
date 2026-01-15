from fastmcp import Context

def get_user(ctx: Context) -> str | None:
    if ctx.request_context:
        context = ctx.request_context
        user = context.request.query_params.get("user")

        return user if user else None
