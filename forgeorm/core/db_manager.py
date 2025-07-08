from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import DB_ENGINE

ADAPTERS = {"sqlite": SQLiteAdapter()}


def get_adapter():
    return ADAPTERS[DB_ENGINE]


def save_instance(instance):
    meta = instance._meta
    fields = meta.fields
    table_name = meta.table_name
    pk_field = meta.primary_key
    pk_value = getattr(instance, pk_field)

    columns = []
    values = []
    placeholders = []

    for name, field in fields.items():
        if name == pk_field and getattr(instance, name) is None:
            continue  # Skip autoincrement PK on insert
        columns.append(field.db_column)
        values.append(getattr(instance, name))
        placeholders.append("?")

    adapter = get_adapter()
    with adapter.connect() as conn:
        cursor = conn.cursor()

        if pk_value is None:
            sql = (
                f"INSERT INTO {table_name} ({', '.join(columns)})"
                f"VALUES ({', '.join(placeholders)})"
            )
            print(f"[ForgeORM] INSERT SQL:\n{sql}\nVALUES: {values}")
            cursor.execute(sql, values)
            instance_id = cursor.lastrowid
            setattr(instance, pk_field, instance_id)
        else:
            set_clause = ", ".join(f"{col}=?" for col in columns)
            sql = (
                f"UPDATE {table_name} SET {set_clause}"
                f"WHERE {fields[pk_field].db_column} = ?"
            )
            print(f"[ForgeORM] UPDATE SQL:\n{sql}\nVALUES: {values + [pk_value]}")
            cursor.execute(sql, values + [pk_value])

        conn.commit()


def fetch_all(model_cls):
    meta = model_cls._meta
    table_name = meta.table_name
    fields = meta.fields

    sql = f"SELECT * FROM {table_name}"

    adapter = get_adapter()
    with adapter.connect() as conn:
        cursor = conn.cursor()
        print(f"[ForgeORM] FETCH ALL SQL:\n{sql}")
        cursor.execute(sql)
        rows = cursor.fetchall()

    return [_build_instance(model_cls, row, fields) for row in rows]


def fetch_filtered(model_cls, **filters):
    meta = model_cls._meta
    table_name = meta.table_name
    fields = meta.fields

    where_clauses = []
    values = []

    for key, value in filters.items():
        field = fields.get(key)
        if not field:
            raise ValueError(f"No such field: {key}")
        where_clauses.append(f"{field.db_column} = ?")
        values.append(value)

    where_sql = " AND ".join(where_clauses)
    sql = f"SELECT * FROM {table_name} WHERE {where_sql}"

    adapter = get_adapter()
    with adapter.connect() as conn:
        cursor = conn.cursor()
        print(f"[ForgeORM] FILTER SQL:\n{sql}\nVALUES: {values}")
        cursor.execute(sql, values)
        rows = cursor.fetchall()

    return [_build_instance(model_cls, row, fields) for row in rows]


def _build_instance(model_cls, row, fields):
    field_names = list(fields.keys())
    kwargs = dict(zip(field_names, row))
    return model_cls(**kwargs)


def delete_instance(instance):
    meta = instance._meta
    table_name = meta.table_name
    pk_field = meta.primary_key
    pk_column = meta.fields[pk_field].db_column
    pk_value = getattr(instance, pk_field)

    if pk_value is None:
        raise ValueError("Cannot delete instance without primary key.")

    sql = f"DELETE FROM {table_name} WHERE {pk_column} = ?"
    print(f"[ForgeORM] DELETE SQL:\n{sql}\nVALUE: {pk_value}")

    adapter = get_adapter()
    with adapter.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (pk_value,))
        conn.commit()
