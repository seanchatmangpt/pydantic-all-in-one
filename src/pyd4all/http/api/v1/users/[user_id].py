# src/pyd4all/http/api/v1/users/[user_id].py

from fastapi import APIRouter, Path

# Define the router for this endpoint
router = APIRouter()


@router.get("")
async def get_user(user_id: int = Path(..., title="User ID", description="The ID of the user to retrieve")):
    """
    Endpoint to retrieve a user by user ID.
    """
    # Dummy user data
    user_data = {"user_id": user_id, "name": "John Doe", "email": "johndoe@example.com"}

    return user_data
