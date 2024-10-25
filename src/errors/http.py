import datetime

from fastapi.exceptions import HTTPException
from fastapi import status


def ModelNotFounded(uncorrected_model: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "ok": False,
            "message": f"Хранилище не содержит модель {uncorrected_model}",
            "time": datetime.datetime.now(datetime.UTC).timestamp()
        }
    )
