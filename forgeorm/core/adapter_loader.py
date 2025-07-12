from forgeorm.adapters.postgres_adapter import PostgresAdapter
from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import get_db_engine, get_db_path, get_postgres_config


def get_adapter():
    engine = get_db_engine()
    if engine == "sqlite":
        return SQLiteAdapter(get_db_path())
    elif engine == "postgres":
        return PostgresAdapter(get_postgres_config())
    else:
        raise ValueError(f"Unsupported DB_ENGINE: {engine}")
