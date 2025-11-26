from forgeorm import get_connection, init
from forgeorm.models.demo_model import Book

# Step 1: Initialize the DB engine
init(
    engine="sqlite",  # ⬅️ Switch to "sqlite" to test another adapter
)

# Step 2: Create the Book table
db = get_connection()
db.create_table(Book)