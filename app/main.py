from fastapi import FastAPI, Response
from app.middleware import AuthMiddleware

app = FastAPI(
    title="Auth Interceptor API",
    description="Intercepta requisicoes e valida um token de acesso no header Authorization antes de chegar aos controllers",
    version="1.0.0",
)

app.add_middleware(AuthMiddleware)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/foo-bar", status_code=204)
def foo_bar():
    return Response(status_code=204)


@app.get("/baz-qux", status_code=204)
def baz_qux():
    return Response(status_code=204)
