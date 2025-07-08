from forgeorm.models.demo_model import Book

# book = Book(
#     title="Truth Unfiltered",
#     description="Raw truth that hurts and heals.",
#     published=True,
#     rating=4.9,
#     release_date="2025-07-08",
#     last_updated="2025-07-08 19:50:00"
# )
# book.save()
#
# books = Book.all()
# print("\n📚 ALL BOOKS:")
# for b in books:
#     print(b)
#
# filtered = Book.filter(published=True)
# print("\n✅ PUBLISHED BOOKS:")
# for b in filtered:
#     print(b)

book = Book(title="V for Victory", published=True)
book.save()  # Should insert

book.title = "V for Vendetta"
book.save()  # Should update

book.delete()  # Should delete
