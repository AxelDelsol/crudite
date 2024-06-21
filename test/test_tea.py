from contextlib import contextmanager

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from crudite.main import app
from crudite.tea import InMemoryTeaStore, Tea, get_tea_store


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@contextmanager
def stub_store(*args: Tea):
    store = InMemoryTeaStore(*args)

    app.dependency_overrides[get_tea_store] = lambda: store
    try:
        yield store
    finally:
        del app.dependency_overrides[get_tea_store]


class TestTea:
    def test_get_tea_returns_tea_1(self, test_client: TestClient):
        tea = Tea(id="1", name="Green", quantity=23)
        with stub_store(tea):
            response = test_client.get(f"/teas/{tea.id}")

            _assert_status_code(response, status.HTTP_200_OK)
            _assert_tea(response, tea)

    def test_get_tea_returns_tea_2(self, test_client: TestClient):
        tea = Tea(id="2", name="Apple", quantity=9)
        with stub_store(tea):
            response = test_client.get(f"/teas/{tea.id}")
            _assert_status_code(response, status.HTTP_200_OK)
            _assert_tea(response, tea)

    def test_unknown_tea_returns_404(self, test_client: TestClient):
        with stub_store():
            response = test_client.get("/teas/42")
            _assert_status_code(response, status.HTTP_404_NOT_FOUND)

    def test_all_teas(self, test_client: TestClient):
        teas = [
            Tea(id="1", name="Green", quantity=23),
            Tea(id="2", name="Apple", quantity=9),
        ]
        with stub_store(*teas):
            response = test_client.get("/teas")

            got = [Tea(**tea) for tea in response.json()["data"]]
            assert got == teas

    def test_create_new_tea(self, test_client: TestClient):
        with stub_store() as store:
            body = {"name": "New tea", "quantity": 20}
            response = test_client.post("/teas", json=body)

            _assert_status_code(response, status.HTTP_201_CREATED)
            got = Tea(**response.json())

            assert store.get_tea(got.id) == got

    def test_delete_tea(self, test_client: TestClient):
        tea = Tea(id="1", name="Green", quantity=23)
        with stub_store(tea) as store:
            response = test_client.delete(f"/teas/{tea.id}")

            _assert_status_code(response, status.HTTP_204_NO_CONTENT)
            assert store.get_tea(tea.id) == None

    def test_delete_tea_returns_404_on_unknown(self, test_client: TestClient):
        with stub_store() as store:
            tea_id = "unknown"
            response = test_client.delete(f"/teas/{tea_id}")

            _assert_status_code(response, status.HTTP_404_NOT_FOUND)
            assert store.get_tea(tea_id) == None

    def test_update_tea(self, test_client: TestClient):
        tea = Tea(id="1", name="Green", quantity=23)
        with stub_store(tea) as store:
            tea_id = tea.id
            body = {"quantity": 42}
            response = test_client.put(f"/teas/{tea_id}", json=body)

            _assert_status_code(response, status.HTTP_200_OK)
            expected_tea = tea.model_copy(update={"quantity": 42})
            _assert_tea(response, expected_tea)
            assert store.get_tea(tea_id) == expected_tea

    def test_update_tea_returns_404_on_unknown(self, test_client: TestClient):
        with stub_store() as store:
            tea_id = "unknown"
            body = {"quantity": 42}
            response = test_client.put(f"/teas/{tea_id}", json=body)

            _assert_status_code(response, status.HTTP_404_NOT_FOUND)
            assert store.get_tea(tea_id) == None


def _assert_tea(response: Response, expected_tea: Tea):
    actual_tea = Tea(**response.json())
    assert actual_tea == expected_tea


def _assert_status_code(response: Response, status_code: int):
    assert response.status_code == status_code
