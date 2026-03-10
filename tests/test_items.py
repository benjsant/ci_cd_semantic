from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Items CRUD API"}


def test_create_item(client: TestClient) -> None:
    response = client.post("/items/", json={"nom": "Laptop", "prix": 999.99})
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Laptop"
    assert data["prix"] == 999.99
    assert "id" in data


def test_create_item_invalid_prix(client: TestClient) -> None:
    response = client.post("/items/", json={"nom": "Laptop", "prix": -10.0})
    assert response.status_code == 422


def test_create_item_empty_nom(client: TestClient) -> None:
    response = client.post("/items/", json={"nom": "", "prix": 100.0})
    assert response.status_code == 422


def test_get_items_empty(client: TestClient) -> None:
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_items(client: TestClient) -> None:
    client.post("/items/", json={"nom": "Écran", "prix": 299.99})
    client.post("/items/", json={"nom": "Clavier", "prix": 79.99})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_items_pagination(client: TestClient) -> None:
    for i in range(5):
        client.post("/items/", json={"nom": f"Item {i}", "prix": float(i + 1)})

    response = client.get("/items/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_item_by_id(client: TestClient) -> None:
    create_response = client.post("/items/", json={"nom": "Souris", "prix": 49.99})
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Souris"
    assert data["prix"] == 49.99


def test_get_item_not_found(client: TestClient) -> None:
    response = client.get("/items/9999")
    assert response.status_code == 404


def test_update_item(client: TestClient) -> None:
    create_response = client.post("/items/", json={"nom": "Vieux PC", "prix": 500.0})
    item_id = create_response.json()["id"]

    response = client.put(f"/items/{item_id}", json={"prix": 350.0})
    assert response.status_code == 200
    data = response.json()
    assert data["prix"] == 350.0
    assert data["nom"] == "Vieux PC"


def test_update_item_nom(client: TestClient) -> None:
    create_response = client.post("/items/", json={"nom": "Ancien nom", "prix": 100.0})
    item_id = create_response.json()["id"]

    response = client.put(f"/items/{item_id}", json={"nom": "Nouveau nom"})
    assert response.status_code == 200
    assert response.json()["nom"] == "Nouveau nom"


def test_update_item_not_found(client: TestClient) -> None:
    response = client.put("/items/9999", json={"prix": 100.0})
    assert response.status_code == 404


def test_delete_item(client: TestClient) -> None:
    create_response = client.post("/items/", json={"nom": "À supprimer", "prix": 1.0})
    item_id = create_response.json()["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client: TestClient) -> None:
    response = client.delete("/items/9999")
    assert response.status_code == 404
