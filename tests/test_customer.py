from fastapi import status

def test_create_customer(client):
    payload = {
        "name": "Alice Smith",
        "phone_number": "+1234567890",
        "email": "alice@example.com"
    }
    response = client.post("/customers", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Alice Smith"
    assert data["phone_number"] == "+1234567890"
    assert "customer_id" in data

def test_create_customer_duplicate_phone(client):
    payload = {
        "name": "Alice Smith",
        "phone_number": "+1234567890",
        "email": "alice@example.com"
    }
    # Create first
    client.post("/customers", json=payload)
    # Create duplicate
    response = client.post("/customers", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_customer(client):
    # Create customer
    customer = client.post("/customers", json={
        "name": "Bob Jones",
        "phone_number": "+0987654321",
        "email": "bob@example.com"
    }).json()

    response = client.get(f"/customers/{customer['customer_id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Bob Jones"

def test_update_customer(client):
    customer = client.post("/customers", json={
        "name": "Charlie Brown",
        "phone_number": "+1122334455",
        "email": "charlie@example.com"
    }).json()

    response = client.put(f"/customers/{customer['customer_id']}", json={
        "name": "Charlie Updated"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Charlie Updated"

def test_delete_customer(client):
    customer = client.post("/customers", json={
        "name": "Delta Fox",
        "phone_number": "+9988776655",
        "email": "delta@example.com"
    }).json()

    response = client.delete(f"/customers/{customer['customer_id']}")
    assert response.status_code == status.HTTP_200_OK
    
    # Try fetching again
    get_res = client.get(f"/customers/{customer['customer_id']}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
