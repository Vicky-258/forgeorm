# config.py

DB_ENGINE = "sqlite"  # "sqlite" or "postgres"
DB_PATH = "forgeorm.db"

POSTGRES_CONFIG = {
    "host": "localhost",
    "dbname": "forgeorm_dev",
    "user": "postgres",
    "password": "postgres258",
    "port": 5432,
}


def get_db_path():
    return DB_PATH


def set_db_path(new_path: str):
    global DB_PATH
    DB_PATH = new_path


def get_db_engine():
    return DB_ENGINE


def set_db_engine(new_engine: str):
    global DB_ENGINE
    DB_ENGINE = new_engine


def get_postgres_config():
    return POSTGRES_CONFIG


def set_postgres_config(new_config: dict):
    global POSTGRES_CONFIG
    POSTGRES_CONFIG = new_config
