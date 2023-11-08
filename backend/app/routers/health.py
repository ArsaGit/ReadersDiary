from fastapi import APIRouter, status, Request

health_router = r = APIRouter()


@r.get("/", status_code=status.HTTP_200_OK)
async def fastapi_check(request: Request):
    return {"message": "Hello World"}
