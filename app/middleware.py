from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.security import validate_token

PUBLIC_PATHS = {"/docs", "/openapi.json", "/redoc", "/health"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not validate_token(token):
            return JSONResponse(
                status_code=401,
                content={
                    "error": "unauthorized",
                    "message": "Token de acesso ausente ou invalido",
                },
            )

        return await call_next(request)
