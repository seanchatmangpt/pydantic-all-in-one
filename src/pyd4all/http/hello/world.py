from fastapi import APIRouter

# Define a router instance for this module
router = APIRouter()

# Endpoint that will be available under the path determined by the filesystem structure
@router.get("")
async def greet():
    return {"message": "Hello, dynamic world!"}


@router.get("/custom")
async def custom_greeting(name: str = "world"):
    return {"message": f"Hello, {name}!"}