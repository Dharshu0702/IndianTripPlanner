"""One-time script to reset a user's password directly in MongoDB."""

import sys
import bcrypt
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/trip_planner"

def reset_password(email, new_password):
    client = MongoClient(MONGO_URI)
    db = client["trip_planner"]

    user = db.users.find_one({"email": email})
    if not user:
        print(f"❌ No user found with email: {email}")
        print("\nExisting users:")
        for u in db.users.find({}, {"email": 1, "name": 1, "role": 1}):
            print(f"  - {u['email']} | {u.get('name','?')} | role: {u.get('role','user')}")
        return

    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    db.users.update_one(
        {"email": email},
        {"$set": {"password": hashed}}   # store as bytes, same as signup
    )
    print(f"✅ Password reset for {email}")
    print(f"   Role: {user.get('role', 'user')}")
    print(f"   New password: {new_password}")

def list_users():
    client = MongoClient(MONGO_URI)
    db = client["trip_planner"]
    print("\n📋 All users in database:\n")
    print(f"{'Email':<35} {'Name':<20} {'Role':<10}")
    print("-" * 65)
    for u in db.users.find({}, {"email": 1, "name": 1, "role": 1, "_id": 0}):
        print(f"{u.get('email','?'):<35} {u.get('name','?'):<20} {u.get('role','user'):<10}")

def promote_to_admin(email):
    client = MongoClient(MONGO_URI)
    db = client["trip_planner"]
    result = db.users.update_one({"email": email}, {"$set": {"role": "admin"}})
    if result.modified_count:
        print(f"✅ {email} is now admin")
    else:
        print(f"❌ User not found: {email}")

if __name__ == "__main__":
    print("=" * 65)
    print("  India Smart Trip Planner — DB Management Tool")
    print("=" * 65)

    # First, list all users
    list_users()

    print("\nOptions:")
    print("  1. Reset password")
    print("  2. Promote user to admin")
    choice = input("\nChoose (1/2): ").strip()

    if choice == "1":
        email = input("Email: ").strip()
        new_pass = input("New password: ").strip()
        reset_password(email, new_pass)

    elif choice == "2":
        email = input("Email to promote: ").strip()
        promote_to_admin(email)
        # Also ask to reset password
        reset = input("Also reset password? (y/n): ").strip().lower()
        if reset == "y":
            new_pass = input("New password: ").strip()
            reset_password(email, new_pass)
