from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping_test():
    return {"message": "pong"}