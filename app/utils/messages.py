from typing import Any
from fastapi import HTTPException, status


def created_success_message(id: str, type: str) -> dict:
    return {"Success": f"A {type} with id -> {id} has been created"}


def server_error(status_code, e) -> dict:
    raise HTTPException(
        status_code=status_code, detail=str(e))


def is_found(data):
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No data found")
    return True


def is_not_found(data, type: str):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{type} item not found")
