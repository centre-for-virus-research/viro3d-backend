from starlette.responses import HTMLResponse
from starlette import status
from fastapi import APIRouter


router = APIRouter(
    prefix="/health_check",
    tags=["Health_check"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", include_in_schema=False)
def health_check():
    return HTMLResponse("success", status_code=status.HTTP_200_OK)