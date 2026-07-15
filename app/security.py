import os

VALID_TOKEN = os.getenv("VALID_TOKEN", "vYQIYxOpyfr==")


def validate_token(token: str) -> bool:
    if not token:
        return False
    return token == VALID_TOKEN
