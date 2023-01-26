import os
from pathlib import Path

import pytz
from sqlalchemy.engine.url import URL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

ENV: str = os.getenv("ENV", "dev")
"""Current environment. Either production (prod and staging) or dev (local and test)."""

# Make sure to use right .env file. Uses .env by default and will use docker env files for docker environment. (Is set in Dockerfile)



p: Path = (
    Path(__file__).parents[4] / ".env"
    if ENV is not None and "docker" not in ENV
    else Path(__file__).parents[4] / f".env-{ENV}"
)
print(f"Using env file: {p.absolute()}" if p.exists() else f"Env file not found: {p.absolute()}")
config: Config = Config(p if p.exists() else None)


def is_production():
    return ENV == "production"


def is_development():
    return ENV == "dev"


def is_test():
    return ENV == "test"


DEFAULT_TIMEZONE_NAME = "Europe/Amsterdam"

DEFAULT_TIMEZONE = pytz.timezone(DEFAULT_TIMEZONE_NAME)

VERSION: str = os.getenv("VERSION", "not set")

APPLICATION_NAME: str = (
    config("APPLICATION_NAME", cast=str, default=os.uname()[1])
    + " - "
    + os.uname()[1]
)

VERSION: str = config("VERSION", cast=str, default="0.1")

MYSQL_USER: str = config("MYSQL_USER", cast=str, default="root")

MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", cast=str, default="root")

MYSQL_ROOT_PASSWORD: str = config("MYSQL_PASSWORD", cast=str, default="root")

MYSQL_DB: str = config("MYSQL_DB", cast=str, default=MYSQL_USER)

MYSQL_HOST: str = config("MYSQL_HOST", cast=str)

MYSQL_PORT: int = config("MYSQL_PORT", cast=int, default=3306)

MYSQL_LOG_SQL: bool = config("MYSQL_LOG_SQL", cast=bool, default=False)

DATABASE_URL: URL = URL(
    "mysql+mysqlconnector",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB,
)


AUTHJWT_SECRET_KEY: str = config("AUTHJWT_SECRET_KEY", cast=str)

URL_TOKEN_SECRET_KEY: str = config("URL_TOKEN_SECRET_KEY", cast=str)

ALLOWED_HOSTS: CommaSeparatedStrings = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="localhost",
)

MYSQL_LOG_SQL: bool = config("MYSQL_LOG_SQL", cast=bool, default=True)
HARVEST_PERSONAL_TOKEN: str = config("HARVEST_PERSONAL_TOKEN", cast=str)
HARVEST_ACCOUNT_ID: str = config("HARVEST_ACCOUNT_ID", cast=str)
