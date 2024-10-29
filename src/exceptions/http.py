from fastapi import status
from fastapi.exceptions import HTTPException

import datetime


def ModelNotFounded(uncorrected_model: str):
    """
    Ошибка в случае запроса не существующей модели
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "ok": False,
            "message": f"Хранилище не содержит модель {uncorrected_model}",
            "time": datetime.datetime.now(datetime.UTC).timestamp()
        }
    )
