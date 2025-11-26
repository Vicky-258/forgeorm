import os
import logging
from forgeorm import init
from forgeorm.core.base_model import BaseModel
from forgeorm.core.fields import IntegerField, CharField, BooleanField
from forgeorm.core.db_manager import get_adapter

# Define a test model
class AppUser(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(max_length=50)
    is_active = BooleanField(default=True)

def run_check():
    print("--- Starting Sanity Check ---")
    
    # Initialize with SQLite
    db_path = "sanity_check.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    # init("sqlite", sqlite_path=db_path, log_level=logging.DEBUG)

    init(
        "postgres",
        postgres_config={
            "dbname": "forge_test",
            "user": "postgres",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
        },
        log_level=logging.DEBUG
    )
    
    adapter = get_adapter()
    print(f"Adapter: {adapter.__class__.__name__}")
    print(f"Param Style: {adapter.param_style}")
    
    # Create Table
    print("\n1. Creating Table...")
    adapter.drop_table(AppUser)
    adapter.create_table(AppUser)
    
    # Insert
    print("\n2. Inserting Users...")
    u1 = AppUser(username="alice", is_active=True)
    u1.save()
    print(f"Saved User 1: ID={u1.id}, Name={u1.username}")
    
    u2 = AppUser(username="bob", is_active=False)
    u2.save()
    print(f"Saved User 2: ID={u2.id}, Name={u2.username}")
    
    # Fetch All
    print("\n3. Fetching All...")
    users = AppUser.all()
    print(f"Found {len(users)} users.")
    for u in users:
        print(f" - {u.username} (Active: {u.is_active})")
        
    # Filter
    print("\n4. Filtering (is_active=True)...")
    active_users = AppUser.filter(is_active=True)
    print(f"Found {len(active_users)} active users.")
    assert len(active_users) == 1
    assert active_users[0].username == "alice"
    
    # Update
    print("\n5. Updating User 2...")
    u2.username = "bobby"
    u2.save()
    
    updated_u2 = AppUser.filter(username="bobby")[0]
    print(f"Updated Name: {updated_u2.username}")
    assert updated_u2.username == "bobby"
    
    # Delete
    print("\n6. Deleting User 1...")
    u1.delete()
    
    remaining = AppUser.all()
    print(f"Remaining users: {len(remaining)}")
    assert len(remaining) == 1
    assert remaining[0].username == "bobby"
    
    print("\n--- Sanity Check Passed! ---")
    
    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    run_check()
