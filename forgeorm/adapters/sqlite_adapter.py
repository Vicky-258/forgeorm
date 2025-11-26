import sqlite3
from typing import TYPE_CHECKING

from .base import BaseAdapter

if TYPE_CHECKING:
    pass


import logging

logger = logging.getLogger(__name__)

class SQLiteAdapter(BaseAdapter):

    def __init__(self, db_path: str = "forgeorm.sqlite3") -> None:
        self.db_path = db_path

    @property
    def param_style(self) -> str:
        return "?"

    def connect(self):
        if isinstance(self.db_path, sqlite3.Connection):
            return self.db_path
        return sqlite3.connect(self.db_path)

    def create_table_sql(self, model_cls) -> str:
        meta = model_cls._meta
        table_name = meta.table_name
        columns = []

        for field in meta.fields.values():
            col_parts = [field.db_column or field.name]
            col_parts.append(field.get_sql_type("sqlite"))

            if field.primary_key:
                col_parts.append("PRIMARY KEY")
            if not field.nullable:
                col_parts.append("NOT NULL")
            if field.default is not None:
                col_parts.append(f"DEFAULT {self._format_default(field.default)}")
            if field.unique:
                col_parts.append("UNIQUE")

            columns.append(" ".join(col_parts))

        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(columns) + "\n);"

    def _format_default(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)

    def create_table(self, model_cls) -> None:
        sql = self.create_table_sql(model_cls)
        with self.connect() as conn:
            cursor = conn.cursor()
            logger.info(f"[ForgeORM] Executing SQL:\n{sql}\n")
            cursor.execute(sql)
            conn.commit()

    def drop_table(self, model_cls) -> None:
        table_name = model_cls._meta.table_name
        sql = f"DROP TABLE IF EXISTS {table_name};"
        with self.connect() as conn:
            cursor = conn.cursor()
            logger.info(f"[ForgeORM] Dropping table if exists:\n{sql}\n")
            cursor.execute(sql)
