from functools import cache
from typing import Annotated, Optional, Protocol
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


class TeaCreate(BaseModel):
    name: str
    quantity: int


class Tea(TeaCreate):
    id: str


class TeaStore(Protocol):
    def get_tea(self, tea_id: str) -> Optional[Tea]:
        """Return a tea based on its id.

        Args:
            tea_id (str): Tea id

        Returns:
            Optional[Tea]: The tea with the associated tea_id or None if not found
        """
        ...

    def save_tea(self, tea: TeaCreate) -> Tea:
        """Save a new tea in the store.

        Args:
            tea (TeaCreate): Tea properties to save

        Returns:
            Tea: The newly saved tea.
        """
        ...

    def delete_tea(self, tea_id: str) -> Optional[Tea]:
        """Delete an existing tea.

        Args:
            tea_id (str): The tea id to delete

        Returns:
            Optional[Tea]: The deleted tea or None if it did not exist
        """
        ...


class InMemoryTeaStore(TeaStore):
    def __init__(self, *args: Tea) -> None:
        self.mapping = {tea.id: tea for tea in args}

    def get_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping.get(tea_id, None)

    def save_tea(self, tea: TeaCreate) -> Tea:
        new_tea = Tea(id=str(uuid4()), **tea.model_dump())
        self.mapping[tea.name] = new_tea
        return new_tea

    def delete_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping.pop(tea_id, None)


@cache
def get_tea_store():
    return InMemoryTeaStore()


router = APIRouter()


@router.get("/teas/{tea_id}")
def get_tea(tea_id: str, tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    tea = tea_store.get_tea(tea_id)

    _assert_tea_presence(tea)
    return tea


@router.post("/teas", status_code=status.HTTP_201_CREATED)
def create_tea(tea: TeaCreate, tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    return tea_store.save_tea(tea)


@router.delete("/teas/{tea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tea(tea_id: str, tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    _assert_tea_presence(tea_store.delete_tea(tea_id))


def _assert_tea_presence(tea: Optional[Tea]):
    if not tea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tea not found"
        )
