DB_ENGINE = "sqlite"
DB_PATH = "forgeorm.db"


def get_db_path():
    return DB_PATH


def set_db_path(new_path: str):
    global DB_PATH
    DB_PATH = new_path
