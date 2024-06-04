from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import get_tea_store
from .store import TeaStore

router = APIRouter()


@router.get("/teas/{tea_id}")
def get_tea(tea_id: str, tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    return tea_store.get_tea(tea_id)
