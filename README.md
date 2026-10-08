# Autenticação — middleware com token fixo

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)

A API não tem usuário nem senha. Um middleware do Starlette lê `Authorization`, aceita o prefixo `Bearer` e compara o valor com `VALID_TOKEN`. A rota só segue se a string for igual.

## Por que token fixo

| Escolha | Efeito |
| --- | --- |
| Comparação com uma variável de ambiente | Sem dependência extra. Não expira, não tem dono, não tem papel. |
| JWT | Expiração e claims, com segredo de assinatura e biblioteca a mais. Este repositório não faz isso. |
| Checagem em cada rota | Fácil esquecer uma rota. O middleware cobre tudo que não está em `PUBLIC_PATHS`. |

Livres: `/docs`, `/openapi.json`, `/redoc`, `/health`. Se `VALID_TOKEN` não estiver definida, `security.py` usa o valor de `.env.example`. Quem clona o repositório conhece esse fallback.

## Stack

- Python (sem versão pinada no repositório)
- FastAPI 0.115.0 e Uvicorn 0.30.6
- Middleware do Starlette, que já vem com o FastAPI

## Estrutura

```
app/
├── main.py        # /health, /foo-bar, /baz-qux
├── middleware.py  # 401 se o token não bater
└── security.py    # comparação com VALID_TOKEN
.env.example
requirements.txt
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/authentication-desafio.git
cd authentication-desafio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export VALID_TOKEN="${VALID_TOKEN:-vYQIYxOpyfr==}"
uvicorn app.main:app --reload
```

Troque `VALID_TOKEN` se não quiser o valor de exemplo.

## Endpoints

| Método | Rota | Auth | Resposta |
| --- | --- | --- | --- |
| GET | `/health` | não | `{"status":"ok"}` |
| GET | `/foo-bar` | sim | 204 |
| GET | `/baz-qux` | sim | 204 |

Token ausente ou diferente: 401 `{"error":"unauthorized","message":"Token de acesso ausente ou invalido"}`.

## O que não tem

Não há testes automatizados, cadastro, refresh, expiração nem hash de segredo.

---

© 2026 Gabriel Teramae Chan
