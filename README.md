# Auth Interceptor API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Starlette](https://img.shields.io/badge/Starlette-Middleware-black?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

Solução para o desafio [`backend-br/desafios/authentication`](https://github.com/backend-br/desafios/blob/master/authentication/PROBLEM.md): interceptar toda requisição HTTP e validar um token de acesso enviado no header `Authorization`, antes que ela chegue a qualquer controller.

## Ideia da solução

A validação acontece num **middleware global** (`AuthMiddleware`), não em cada rota individualmente. Isso garante o requisito principal do desafio: a implementação continua funcionando corretamente mesmo com a adição de novos endpoints, sem precisar tocar em nada além do próprio middleware.

```
Request -> AuthMiddleware.dispatch() -> valida header Authorization -> valido?  -> segue pro controller
                                                                     -> invalido? -> 401 Unauthorized
```

A lógica de validação do token fica isolada em `security.py`, então trocar o mock por uma verificação real (JWT, chamada a um serviço de auth, etc.) é uma mudança local, sem impacto no restante da aplicação.

## Stack

- **FastAPI** para a API REST
- **Starlette `BaseHTTPMiddleware`** para interceptar as requisições antes do roteamento
- Validação de token mockada e isolada em `security.py` (fácil de substituir por uma implementação real)

## Estrutura

```
app/
├── main.py         # app FastAPI + endpoints de exemplo
├── middleware.py     # AuthMiddleware, intercepta toda requisição
└── security.py         # validate_token(), lógica de validação (mock)
```

## Como rodar

```bash
git clone <seu-repo>
cd auth-transparent-api
pip install -r requirements.txt

export VALID_TOKEN=vYQIYxOpyfr==

uvicorn app.main:app --reload --port 8001
```

## Endpoints

| Método | Rota        | Protegido | Descrição                    |
|--------|-------------|:---------:|--------------------------------|
| GET    | `/health`     | Não        | Healthcheck público             |
| GET    | `/foo-bar`     | Sim         | Endpoint de exemplo (204)        |
| GET    | `/baz-qux`      | Sim          | Segundo endpoint, comprova que o middleware protege qualquer rota nova automaticamente |

## Exemplo

Sem token ou com token inválido:

```bash
curl -i http://localhost:8001/foo-bar
```
```
HTTP/1.1 401 Unauthorized
{"error": "unauthorized", "message": "Token de acesso ausente ou invalido"}
```

Com token válido:

```bash
curl -i http://localhost:8001/foo-bar -H "Authorization: vYQIYxOpyfr=="
```
```
HTTP/1.1 204 No Content
```

## Deploy

Pronto para subir no [Railway](https://railway.app): start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, variável de ambiente `VALID_TOKEN` configurada no serviço.

---

© 2026 Gabriel Teramae Chan
