from forgeorm.config.settings import (
    set_db_engine,
    set_db_path,
    set_postgres_config,
)
from forgeorm.core.adapter_loader import get_adapter

__version__ = "0.1.0"  # Optional versioning


import logging

def init(engine="sqlite", sqlite_path="forgeorm.sqlite3", postgres_config=None, log_level=logging.INFO):
    """
    Initializes ForgeORM with the specified database engine and config.

    Args:
        engine (str): "sqlite" or "postgres"
        sqlite_path (str): Path to SQLite database file
        postgres_config (dict): Dict with host, dbname, user, password, port
        log_level (int): Logging level (default: logging.INFO)
    """
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    engine = engine.lower()
    set_db_engine(engine)

    if engine == "sqlite":
        set_db_path(sqlite_path)
    elif engine == "postgres":
        if not postgres_config:
            raise ValueError(
                "Postgres config must be provided when engine is 'postgres'"
            )
        set_postgres_config(postgres_config)
    else:
        raise ValueError(f"Unsupported engine: {engine}")


def get_connection():
    """
    Returns the currently configured adapter.
    """
    return get_adapter()
