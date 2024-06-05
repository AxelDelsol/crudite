import io

from crudite.tea.models import Tea
from crudite.tea.store import FileTeaStore


def test_get_tea():
    data = """
{
    "1": {"name": "Green", "quantity": 19}
}
"""
    text_io = io.StringIO(data)
    file_store = FileTeaStore(text_io)
    assert file_store.get_tea("1") == Tea(name="Green", quantity=19)


def test_unknown_tea_returns_none():
    data = """
{
    "1": {"name": "Green", "quantity": 19}
}
"""
    text_io = io.StringIO(data)
    file_store = FileTeaStore(text_io)
    assert file_store.get_tea("2") == None
