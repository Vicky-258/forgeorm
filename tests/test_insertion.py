from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import set_db_path
from forgeorm.core.base_model import BaseModel
from forgeorm.core.db_manager import save_instance
from forgeorm.core.fields import CharField, IntegerField


def setup_function():
    set_db_path(":memory:")
    adapter = SQLiteAdapter()
    InsertModel._meta.adapter = adapter
    adapter.drop_table(InsertModel)  # Add drop_table in your adapter!
    adapter.create_table(InsertModel)


class InsertModel(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)


def test_insertion():
    adapter = InsertModel._meta.adapter  # Already set via setup
    obj = InsertModel(name="Test Guy")
    save_instance(obj)

    with adapter.connect() as conn:
        cursor = conn.execute("SELECT * FROM insertmodel")
        row = cursor.fetchone()
        assert row is not None
        assert row[1] == "Test Guy"
