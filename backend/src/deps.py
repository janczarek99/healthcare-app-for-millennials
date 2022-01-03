from fastapi import Request


async def get_pwd_context(request: Request):
    return request.app.pwd_context
