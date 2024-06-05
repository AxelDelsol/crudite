from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import get_tea_store
from .store import TeaStore

router = APIRouter()


@router.get("/teas/{tea_id}")
def get_tea(tea_id: str, tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    tea = tea_store.get_tea(tea_id)

    if not tea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tea not found"
        )
    return tea
