from fastapi import Request
from fastapi.responses import JSONResponse
from authx.exceptions import MissingTokenError

async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Missing token"},
    )



