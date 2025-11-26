class QueryBuilder:
    def __init__(self, param_style: str):
        self.param_style = param_style

    def build_insert(self, table_name: str, columns: list, pk_column: str = None) -> str:
        placeholders = [self.param_style] * len(columns)
        cols_str = ", ".join(columns)
        vals_str = ", ".join(placeholders)
        sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({vals_str})"
        
        # Simple heuristic: if Postgres (%s), use RETURNING
        if self.param_style == "%s" and pk_column:
            sql += f" RETURNING {pk_column}"
            
        return sql

    def build_update(self, table_name: str, columns: list, pk_column: str) -> str:
        set_clause = ", ".join(f"{col}={self.param_style}" for col in columns)
        return f"UPDATE {table_name} SET {set_clause} WHERE {pk_column} = {self.param_style}"

    def build_select(self, table_name: str, filter_columns: list = None) -> str:
        sql = f"SELECT * FROM {table_name}"
        if filter_columns:
            conditions = [f"{col} = {self.param_style}" for col in filter_columns]
            sql += " WHERE " + " AND ".join(conditions)
        return sql

    def build_delete(self, table_name: str, pk_column: str) -> str:
        return f"DELETE FROM {table_name} WHERE {pk_column} = {self.param_style}"
