from functools import cache

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from crudite.main import app
from crudite.tea import InMemoryTeaStore, Tea, get_tea_store


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@cache
def override_get_tea_store() -> InMemoryTeaStore:
    return InMemoryTeaStore(
        Tea(id="1", name="Green", quantity=23),
        Tea(id="2", name="Apple", quantity=9),
    )


app.dependency_overrides[get_tea_store] = override_get_tea_store


class TestTea:
    def test_get_tea_returns_tea_1(self, test_client: TestClient):
        response = test_client.get("/teas/1")

        _assert_status_code(response, status.HTTP_200_OK)
        _assert_tea(response, Tea(id="1", name="Green", quantity=23))

    def test_get_tea_returns_tea_2(self, test_client: TestClient):
        response = test_client.get("/teas/2")
        _assert_status_code(response, status.HTTP_200_OK)
        _assert_tea(response, Tea(id="2", name="Apple", quantity=9))

    def test_unknown_tea_returns_404(self, test_client: TestClient):
        response = test_client.get("/teas/42")
        _assert_status_code(response, status.HTTP_404_NOT_FOUND)

    def test_create_new_tea(self, test_client: TestClient):
        body = {"name": "New tea", "quantity": 20}
        response = test_client.post("/teas", json=body)

        _assert_status_code(response, status.HTTP_201_CREATED)
        got = Tea(**response.json())
        assert got.name == "New tea"
        assert got.quantity == 20

    def test_delete_tea(self, test_client: TestClient):
        store = override_get_tea_store()
        tea_id = "1"
        response = test_client.delete(f"/teas/{tea_id}")

        _assert_status_code(response, status.HTTP_204_NO_CONTENT)
        assert store.get_tea(tea_id) == None

    def test_delete_tea_returns_404_on_unknown(self, test_client: TestClient):
        store = override_get_tea_store()
        tea_id = "unknown"
        response = test_client.delete(f"/teas/{tea_id}")

        _assert_status_code(response, status.HTTP_404_NOT_FOUND)
        assert store.get_tea(tea_id) == None


def _assert_tea(response: Response, expected_tea: Tea):
    actual_tea = Tea(**response.json())
    assert actual_tea == expected_tea


def _assert_status_code(response: Response, status_code: int):  # type: ignore
    assert response.status_code == status_code
