from fastapi import status

def test_create_customer(client):
    payload = {
        "name": "Jane Doe",
        "phone": "+1999888777",
        "email": "jane@example.com"
    }
    response = client.post("/customers/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["phone"] == "+1999888777"
    assert "id" in data

def test_create_customer_duplicate_phone(client):
    payload = {
        "name": "Jane Doe",
        "phone": "+1999888777",
        "email": "jane@example.com"
    }
    # Create first customer
    client.post("/customers/", json=payload)
    
    # Attempt duplicate creation
    response = client.post("/customers/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_get_customer(client):
    # Setup
    payload = {"name": "Alice", "phone": "+111222333"}
    setup_resp = client.post("/customers/", json=payload).json()
    customer_id = setup_resp["id"]

    # Test
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Alice"

def test_update_customer(client):
    # Setup
    payload = {"name": "Bob", "phone": "+444555666"}
    setup_resp = client.post("/customers/", json=payload).json()
    customer_id = setup_resp["id"]

    # Test update
    update_payload = {"name": "Robert", "email": "robert@example.com"}
    response = client.put(f"/customers/{customer_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Robert"
    assert response.json()["email"] == "robert@example.com"

def test_delete_customer(client):
    # Setup
    payload = {"name": "Dave", "phone": "+777888999"}
    setup_resp = client.post("/customers/", json=payload).json()
    customer_id = setup_resp["id"]

    # Test delete
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify 404
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
