from functools import cache

from .store import FileTeaStore, TeaStore

DB_FILE = "data.json"


@cache
def get_tea_store() -> TeaStore:
    with open(DB_FILE) as f:
        return FileTeaStore(f)
