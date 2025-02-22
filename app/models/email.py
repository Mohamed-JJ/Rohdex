# add your models here
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List, Optional

class ProccessedEmails(BaseModel):
    id: int
    email: str
    body: str

# Load users from the JSON file
def load_users():
    with open("db/emails.json", "r") as f:
        return json.load(f)

# Save users to the JSON file
def save_users(users):
    with open("db/emails.json", "w") as f:
        json.dump(users, f, indent=4)

# Function to create a user
def create_user(user: ProccessedEmails) -> ProccessedEmails:
    users = load_users()
    if any(u.id == user.id for u in users):
        raise ValueError("User ID already exists")
    
    users.append(user)
    save_users(users)
    return user

# Function to retrieve all users
def read_users() -> List[ProccessedEmails]:
    return load_users()

# Function to retrieve a user by ID
def read_user(user_id: int) -> Optional[ProccessedEmails]:
    users = load_users()
    user = next((u for u in users if u.id == user_id), None)
    return user

# Function to delete a user by ID
def delete_user(user_id: int) -> dict:
    users = load_users()
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise ValueError("User not found")
    
    users.remove(user)
    save_users(users)
    return {"detail": "User deleted successfully"}