import psycopg2

from .base import BaseAdapter


class PostgresAdapter(BaseAdapter):
    def __init__(self, db_config: dict):
        self.db_config = db_config  # expects dict with host, dbname, user, password

    def connect(self):
        return psycopg2.connect(**self.db_config)

    def get_sql_type(self, py_type):
        type_map = {int: "INTEGER", float: "REAL", str: "TEXT", bool: "BOOLEAN"}
        return type_map.get(py_type, "TEXT")

    def _format_default(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        else:
            return str(value)

    def create_table_sql(self, model_cls) -> str:
        meta = model_cls._meta
        table_name = meta.table_name
        columns = []

        for field in meta.fields.values():
            col_parts = [field.db_column or field.name]
            col_parts.append(self.get_sql_type(field.field_type))

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

    def create_table(self, model_cls):
        sql = self.create_table_sql(model_cls)
        with self.connect() as conn:
            cursor = conn.cursor()
            print(f"[ForgeORM] Executing PostgreSQL SQL:\n{sql}\n")
            cursor.execute(sql)
            conn.commit()

    def drop_table(self, model_cls):
        table_name = model_cls._meta.table_name
        sql = f"DROP TABLE IF EXISTS {table_name};"
        with self.connect() as conn:
            cursor = conn.cursor()
            print(f"[ForgeORM] Dropping PostgreSQL table:\n{sql}\n")
            cursor.execute(sql)
            conn.commit()
