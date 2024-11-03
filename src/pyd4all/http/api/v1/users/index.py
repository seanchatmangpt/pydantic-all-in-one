# src/pyd4all/http/api/v1/users/index.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Define the router for this endpoint
router = APIRouter()


# Define a Pydantic model for the user input
class UserCreateRequest(BaseModel):
    name: str
    email: str


# Example of in-memory storage for simplicity (use a database in real applications)
fake_user_db = []


@router.post("")
async def create_user(user: UserCreateRequest):
    """
    Endpoint to create a new user.
    """
    # Dummy logic to add user to the database
    new_user = {"id": len(fake_user_db) + 1, "name": user.name, "email": user.email}
    fake_user_db.append(new_user)

    return {"message": "User created successfully", "user": new_user}
