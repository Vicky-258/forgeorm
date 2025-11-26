# cli/test_crud.py
from forgeorm.core.base_model import BaseModel
from forgeorm.core.fields import IntegerField, TextField
from forgeorm.core.db_manager import save_instance, fetch_all, fetch_filtered, delete_instance


# Define a simple model
class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    age = IntegerField()


def run_crud_test():
    print("\n--- ForgeORM CRUD Test ---\n")

    # 1. Insert
    user = User(name="Vicky", age=21)
    save_instance(user)
    print(f"Inserted User: {user.__dict__}")

    # 2. Fetch all
    all_users = fetch_all(User)
    print(f"Fetch all: {[u.__dict__ for u in all_users]}")

    # 3. Update
    user.age = 22
    save_instance(user)
    updated_users = fetch_all(User)
    print(f"After update: {[u.__dict__ for u in updated_users]}")

    # 4. Filter
    filtered = fetch_filtered(User, name="Vicky")
    print(f"Filtered by name: {[u.__dict__ for u in filtered]}")

    # 5. Delete
    delete_instance(user)
    print(f"Deleted User with id={user.id}")

    # 6. Confirm empty
    final_users = fetch_all(User)
    print(f"Final fetch all: {final_users}")


if __name__ == "__main__":
    run_crud_test()
