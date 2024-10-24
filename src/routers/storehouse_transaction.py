from fastapi import APIRouter


router = APIRouter(prefix="/storehouse", tags=["Storehouse"])


@router.get("/", status_code=200)
def get_transaction():
    pass
