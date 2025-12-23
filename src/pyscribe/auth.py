from __future__ import annotations

import keyring

SERVICE_NAME = "pyscribe"
USERNAME = "api_key"


def get_keyring_api_key() -> str | None:
    return keyring.get_password(SERVICE_NAME, USERNAME)


def set_keyring_api_key(api_key: str) -> None:
    keyring.set_password(SERVICE_NAME, USERNAME, api_key)
