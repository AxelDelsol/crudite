import io
import json
from typing import Dict, Optional, Protocol

from .models import Tea


class TeaStore(Protocol):
    def get_tea(self, tea_id: str) -> Optional[Tea]: ...


class FileTeaStore:
    def __init__(self, io: io.TextIOBase) -> None:
        self.data: Dict[str, Tea] = {}
        for key, value in json.load(io).items():
            self.data[key] = Tea(**value)

    def get_tea(self, tea_id: str) -> Optional[Tea]:
        return self.data.get(tea_id, None)
