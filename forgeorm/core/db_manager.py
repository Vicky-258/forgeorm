import logging
from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.adapters.postgres_adapter import PostgresAdapter
import forgeorm.config.settings as settings
from forgeorm.core.query_builder import QueryBuilder

# Configure logger
logger = logging.getLogger(__name__)

# Cache for adapters
_ADAPTER_INSTANCES = {}

def get_adapter():
    engine = settings.DB_ENGINE
    
    if engine == "sqlite":
        # Check if we need to update the adapter (path might have changed)
        current_path = settings.DB_PATH
        if "sqlite" not in _ADAPTER_INSTANCES or _ADAPTER_INSTANCES["sqlite"].db_path != current_path:
            _ADAPTER_INSTANCES["sqlite"] = SQLiteAdapter(db_path=current_path)
        return _ADAPTER_INSTANCES["sqlite"]
        
    elif engine == "postgres":
        # Check if we need to update the adapter (config might have changed)
        current_config = settings.POSTGRES_CONFIG
        # Simple check: just recreate if it doesn't exist. 
        # For a robust check we'd compare configs, but let's just assume if it exists it's good 
        # unless we want to support runtime config changes strictly.
        # Given the "minimal" scope, let's just create it if missing.
        if "postgres" not in _ADAPTER_INSTANCES:
             _ADAPTER_INSTANCES["postgres"] = PostgresAdapter(db_config=current_config)
        return _ADAPTER_INSTANCES["postgres"]
    
    raise ValueError(f"Unsupported DB_ENGINE: {engine}")


def _log_query(prefix: str, sql: str, values=None):
    """Helper for consistent debug logging."""
    logger.info(f"[ForgeORM] {prefix} SQL:\n{sql}")
    if values:
        logger.info(f"VALUES: {values}")


def save_instance(instance):
    """Insert or update a model instance in the database."""
    meta = instance._meta
    fields = meta.fields
    table_name = meta.table_name
    pk_field = meta.primary_key
    pk_value = getattr(instance, pk_field)

    adapter = get_adapter()
    qb = QueryBuilder(adapter.param_style)

    columns, values = [], []

    # Identify columns to save
    for name, field in fields.items():
        if name == pk_field and pk_value is None:
            continue  # Skip autoincrement PK on insert
        columns.append(field.db_column)
        values.append(getattr(instance, name))

    with adapter.connect() as conn:
        cursor = conn.cursor()

        if pk_value is None:
            # INSERT
            pk_col = fields[pk_field].db_column
            sql = qb.build_insert(table_name, columns, pk_column=pk_col)
            _log_query("INSERT", sql, values)
            cursor.execute(sql, values)
            
            # Fetch the new PK
            if adapter.param_style == "%s":
                # Postgres with RETURNING
                new_id = cursor.fetchone()[0]
                setattr(instance, pk_field, new_id)
            elif hasattr(cursor, 'lastrowid'):
                # SQLite
                setattr(instance, pk_field, cursor.lastrowid)
        else:
            # UPDATE
            pk_col = fields[pk_field].db_column
            sql = qb.build_update(table_name, columns, pk_col)
            # Add PK value to the end of values list for the WHERE clause
            _log_query("UPDATE", sql, values + [pk_value])
            cursor.execute(sql, values + [pk_value])

        conn.commit()


def fetch_all(model_cls):
    """Fetch all rows of a given model."""
    meta = model_cls._meta
    adapter = get_adapter()
    qb = QueryBuilder(adapter.param_style)
    
    sql = qb.build_select(meta.table_name)

    with adapter.connect() as conn:
        cursor = conn.cursor()
        _log_query("FETCH ALL", sql)
        cursor.execute(sql)
        rows = cursor.fetchall()

    return [_build_instance(model_cls, row, meta.fields) for row in rows]


def fetch_filtered(model_cls, **filters):
    """Fetch rows filtered by given field=value pairs."""
    meta = model_cls._meta
    fields = meta.fields
    adapter = get_adapter()
    qb = QueryBuilder(adapter.param_style)

    filter_cols, values = [], []
    for key, value in filters.items():
        field = fields.get(key)
        if not field:
            raise ValueError(f"No such field: {key}")
        filter_cols.append(field.db_column)
        values.append(value)

    sql = qb.build_select(meta.table_name, filter_cols)

    with adapter.connect() as conn:
        cursor = conn.cursor()
        _log_query("FILTER", sql, values)
        cursor.execute(sql, values)
        rows = cursor.fetchall()

    return [_build_instance(model_cls, row, fields) for row in rows]


def delete_instance(instance):
    """Delete a model instance by primary key."""
    meta = instance._meta
    pk_field = meta.primary_key
    pk_column = meta.fields[pk_field].db_column
    pk_value = getattr(instance, pk_field)

    if pk_value is None:
        raise ValueError("Cannot delete instance without primary key.")

    adapter = get_adapter()
    qb = QueryBuilder(adapter.param_style)
    
    sql = qb.build_delete(meta.table_name, pk_column)

    with adapter.connect() as conn:
        cursor = conn.cursor()
        _log_query("DELETE", sql, [pk_value])
        cursor.execute(sql, (pk_value,))
        conn.commit()


def _build_instance(model_cls, row, fields):
    """Rebuild a model instance from DB row."""
    field_names = list(fields.keys())
    kwargs = dict(zip(field_names, row))
    return model_cls(**kwargs)
