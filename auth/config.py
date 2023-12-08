import os
from typing import List

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

    secret_key: str = (
        "django-insecure-5-wh%*_hny_@&#b+7+snq*)tik)a-+q@#()^qlpgeco2f8q&*8"
    )
    debug: bool = True
    allowed_hosts: list = []

    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int = 5432

    # whether to require emails to verify their email address
    # valid values: "mandatory", "optional", or "none"
    account_email_verification: str = "none"

    # default protocol for allauth-generated URLs, either "http" or "https"
    account_default_http_protocol: str = "http"

    email_host: str = ""
    email_port: int = 587
    email_host_user: str = ""
    email_host_password: str = ""
    email_backend: str = ""

    admins: List[tuple] = []

    csrf_cookie_domain: str
    csrf_cookie_secure: bool
    csrf_trusted_origins: List[str] = []
    csrf_use_sessions: bool
    session_cookie_domain: str
    session_cookie_secure: bool

    signing_key: str
    verifying_key: str
    issuer: str


# Lazily initialize the config variable using module-level __getattr__
# so that we can import the Config class without triggering config load.
_config = None


def __getattr__(name):
    if name == "config":
        global _config
        if _config is None:
            _config = load_config()
        return _config
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def load_config():
    env_file = os.getenv("ENV_FILE", ".env")
    return Config(_env_file=env_file)
