import pytest

from forgeorm.adapters.sqlite_adapter import SQLiteAdapter
from forgeorm.config.settings import set_db_path
from forgeorm.core.db_manager import fetch_all, fetch_filtered
from forgeorm.models.demo_model import Book


@pytest.fixture(autouse=True)
def setup_db():
    set_db_path(":memory:")
    adapter = SQLiteAdapter()
    Book._meta.adapter = adapter

    with adapter.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS book")

    adapter.create_table(Book)

    # Insert test data
    Book(title="Book A", published=True).save()
    Book(title="Book B", published=False).save()
    Book(title="Book C", published=True).save()


def test_fetch_all_returns_all_books():
    books = fetch_all(Book)
    titles = [b.title for b in books]
    assert set(titles) == {"Book A", "Book B", "Book C"}


def test_filter_returns_correct_subset():
    published_books = fetch_filtered(Book, published=True)
    assert len(published_books) == 2
    assert all(b.published for b in published_books)

    unpublished_books = fetch_filtered(Book, published=False)
    assert len(unpublished_books) == 1
    assert not unpublished_books[0].published


def test_filter_on_nonexistent_field_raises():
    with pytest.raises(ValueError):
        fetch_filtered(Book, non_field="value")
