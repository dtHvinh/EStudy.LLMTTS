from fastapi import APIRouter, Request, HTTPException

test_router = APIRouter()


@test_router.get("/ping", summary="Health check endpoint")
async def ping():
    return {"message": "pong"}
