from pydantic import BaseModel


class Tea(BaseModel):
    name: str
    quantity: int = 0
