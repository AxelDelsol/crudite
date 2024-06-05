from typing import Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from crudite.main import app
from crudite.tea.dependencies import get_tea_store
from crudite.tea.models import Tea
from crudite.tea.store import TeaStore

from .asserts import *


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

        assert_status_code(response, status.HTTP_200_OK)
        assert_tea(response, Tea(name="Green", quantity=23))

    def test_get_tea_returns_tea_2(self, test_client: TestClient):
        response = test_client.get("/teas/2")
        assert_status_code(response, status.HTTP_200_OK)
        assert_tea(response, Tea(name="Apple", quantity=9))

    def test_unknown_tea_returns_404(self, test_client: TestClient):
        response = test_client.get("/teas/42")
        assert_status_code(response, status.HTTP_404_NOT_FOUND)


class InMemoryTeaStore:
    def __init__(self, mapping: Dict[str, Tea]) -> None:
        self.mapping = mapping

    def get_tea(self, tea_id: str) -> Optional[Tea]:
        return self.mapping.get(tea_id, None)
