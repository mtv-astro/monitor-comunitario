from fastapi.testclient import TestClient

from monitor_comunitario.api.main import app

client = TestClient(app)


def test_create_and_get_user() -> None:
    payload = {
        "name": "Carlos Selva",
        "phone": "5548999999999",
        "municipality": "Florianópolis",
        "neighborhood": "Campeche",
        "street": "Avenida Pequeno Príncipe",
        "number": "100",
        "zipcode": "88063-000",
        "accept_municipality_wide_alerts": True,
    }

    create_response = client.post("/users", json=payload)

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["id"] >= 1
    assert created["name"] == payload["name"]
    assert created["municipality"] == payload["municipality"]
    assert created["is_active"] is True

    get_response = client.get(f"/users/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_update_user() -> None:
    create_response = client.post(
        "/users",
        json={
            "name": "Teste Update",
            "phone": "5548999999998",
            "municipality": "São José",
        },
    )

    user_id = create_response.json()["id"]

    update_response = client.patch(
        f"/users/{user_id}",
        json={"neighborhood": "Kobrasol", "street": "Rua Koesa"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["neighborhood"] == "Kobrasol"
    assert update_response.json()["street"] == "Rua Koesa"


def test_deactivate_user() -> None:
    create_response = client.post(
        "/users",
        json={
            "name": "Teste Delete",
            "phone": "5548999999997",
            "municipality": "Palhoça",
        },
    )

    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["is_active"] is False
