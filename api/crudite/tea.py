from functools import cache
from typing import Annotated, Optional, Protocol
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


class TeaCreate(BaseModel):
    name: str
    quantity: int


class TeaUpdate(BaseModel):
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

    def get_teas(self) -> list[Tea]:
        """Return all teas in the store

        Returns:
            list[Tea]: Teas
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

    def update_tea(self, tea_id: str, tea_update: TeaUpdate) -> Optional[Tea]:
        """Update a tea with new attributes

        Args:
            tea_id (str): Tea id to update
            tea_update (TeaUpdate): Attributes to update


        Returns:
            Optional[Tea]: Return the update tea or None if not found
        """
        ...


class InMemoryTeaStore:
    def __init__(self, *args: Tea) -> None:
        self.set_teas(*args)

    def set_teas(self, *args: Tea) -> None:
        self.mapping = {tea.id: tea for tea in args}

    def get_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping.get(tea_id, None)

    def get_teas(self) -> list[Tea]:
        return list(self.mapping.values())

    def save_tea(self, tea: TeaCreate) -> Tea:
        id = str(uuid4())
        new_tea = Tea(id=id, **tea.model_dump())
        self.mapping[id] = new_tea
        return new_tea

    def delete_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping.pop(tea_id, None)

    def update_tea(self, tea_id: str, tea_update: TeaUpdate) -> Optional[Tea]:
        existing_tea = self.get_tea(tea_id)

        if existing_tea:
            updated_tea = existing_tea.model_copy(update=tea_update.model_dump())
            self.mapping[tea_id] = updated_tea
            return updated_tea


store = InMemoryTeaStore()


@cache
def get_tea_store() -> TeaStore:
    return store


router = APIRouter()


@router.get("/teas")
def get_teas(tea_store: Annotated[TeaStore, Depends(get_tea_store)]):
    teas = tea_store.get_teas()

    return {"data": teas}


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


@router.put("/teas/{tea_id}")
def update_tea(
    tea_id: str, tea: TeaUpdate, tea_store: Annotated[TeaStore, Depends(get_tea_store)]
):
    updated_tea = tea_store.update_tea(tea_id, tea)

    _assert_tea_presence(updated_tea)
    return updated_tea


def _assert_tea_presence(tea: Optional[Tea]):
    if not tea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tea not found"
        )
