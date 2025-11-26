import pytest

from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import set_db_path
from forgeorm.core.fields import CharField
from forgeorm.models.demo_model import Book


@pytest.fixture(autouse=True)
def setup_db():
    set_db_path(":memory:")
    adapter = SQLiteAdapter()
    Book._meta.adapter = adapter
    adapter.drop_table(Book)  # Assuming you added this method!
    adapter.create_table(Book)
    yield
    # Optional teardown


def test_meta_table_name():
    assert Book._meta.table_name == "book"


def test_field_names_mapped_correctly():
    field_names = Book._meta.fields.keys()
    assert "title" in field_names
    assert "published" in field_names


def test_field_instance_types():
    assert isinstance(Book._meta.fields["title"], CharField)


def test_primary_key_field_set():
    assert Book._meta.primary_key == "id"
