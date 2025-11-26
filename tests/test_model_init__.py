from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import set_db_path
from forgeorm.models.demo_model import Book


def setup_function():
    set_db_path(":memory:")  # or "test.db" if you want a file
    adapter = SQLiteAdapter(":memory:")
    with adapter.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS book")
        # Or call adapter.create_table(Book) if you have that


def test_model_instantiation_with_kwargs():
    book = Book(title="1984", published=True)
    assert book.title == "1984"
    assert book.published is True
    assert book.id is None  # Shouldn't be set until saved


def test_model_default_values_applied():
    book = Book(title="Untitled")
    assert book.rating == 4.5  # Default in model
    assert book.published is False  # Default in field definition


def test_repr_contains_class_name_and_fields():
    book = Book(title="Sapiens", published=False)
    r = repr(book)
    assert "Book" in r
    assert "title='Sapiens'" in r
