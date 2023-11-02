from fastapi import APIRouter, status, Request

router = APIRouter()


@router.get("/fastapi", status_code=status.HTTP_200_OK)
async def fastapi_check(request: Request):
    return {
        "status": "OK"
    }
