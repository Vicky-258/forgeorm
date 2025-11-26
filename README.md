# ForgeORM

A lightweight, blazing-fast ORM designed to simplify model definitions and scale seamlessly across databases (SQLite & PostgreSQL).

## Features
- **Multi-DB Support**: Switch between SQLite and PostgreSQL with a single config change.
- **Simple Models**: Define models using standard Python classes and fields.
- **CRUD Operations**: Save, filter, fetch all, and delete records easily.
- **Logging**: Built-in logging for SQL queries.

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Define a Model
```python
from forgeorm.core.base_model import BaseModel
from forgeorm.core.fields import IntegerField, CharField, BooleanField

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=50)
    is_active = BooleanField(default=True)
```

### 3. Initialize and Use
```python
from forgeorm import init
from forgeorm.core.db_manager import get_adapter

# Initialize (SQLite)
init("sqlite", sqlite_path="my_database.db")

# Or Initialize (PostgreSQL)
# init("postgres", postgres_config={"host": "localhost", "dbname": "mydb", "user": "user", "password": "pw"})

# Create Table (Manual for now)
adapter = get_adapter()
adapter.create_table(User)

# Create
user = User(username="alice")
user.save()

# Read
all_users = User.all()
active_users = User.filter(is_active=True)

# Update
user.username = "alice_new"
user.save()

# Delete
user.delete()
```
