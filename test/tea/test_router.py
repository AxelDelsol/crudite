from typing import Dict, Optional

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from crudite.main import app
from crudite.tea.dependencies import get_tea_store
from crudite.tea.models import Tea
from crudite.tea.store import TeaStore


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


def override_get_tea_store() -> TeaStore:
    mapping = {"1": Tea(name="Green", quantity=23), "2": Tea(name="Apple", quantity=9)}
    return InMemoryTeaStore(mapping)


app.dependency_overrides[get_tea_store] = override_get_tea_store


class TestTea:
    def test_get_tea_returns_tea_1(self, test_client: TestClient):
        response = test_client.get("/teas/1")
        assert_tea(response, Tea(name="Green", quantity=23))

    def test_get_tea_returns_tea_2(self, test_client: TestClient):
        response = test_client.get("/teas/2")
        assert_tea(response, Tea(name="Apple", quantity=9))


def assert_tea(response: Response, expected_tea: Tea):
    actual_tea = Tea(**response.json())
    assert actual_tea == expected_tea


class InMemoryTeaStore:
    def __init__(self, mapping: Dict[str, Tea]) -> None:
        self.mapping = mapping

    def get_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping[tea_id]
