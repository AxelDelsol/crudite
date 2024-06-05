from httpx import Response

from crudite.tea.models import Tea


def assert_tea(response: Response, expected_tea: Tea):
    actual_tea = Tea(**response.json())
    assert actual_tea == expected_tea


def assert_status_code(response: Response, status_code: int):  # type: ignore
    assert response.status_code == status_code
