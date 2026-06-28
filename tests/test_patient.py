from fastapi import status

def test_create_patient(client):
    payload = {
        "name": "Rahul",
        "phone_number": "+919876543210",
        "email": "rahul@example.com",
        "gender": "Male",
        "age": 28
    }
    response = client.post("/patients/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Rahul"
    assert data["phone_number"] == "+919876543210"
    assert "patient_id" in data

def test_create_patient_duplicate_phone(client):
    payload = {
        "name": "Rahul",
        "phone_number": "+919876543210",
        "email": "rahul@example.com",
        "gender": "Male",
        "age": 28
    }
    # Create first patient
    client.post("/patients/", json=payload)
    
    # Attempt duplicate creation
    response = client.post("/patients/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_get_patient(client):
    # Setup
    payload = {"name": "Alice", "phone_number": "+111222333"}
    setup_resp = client.post("/patients/", json=payload).json()
    patient_id = setup_resp["patient_id"]

    # Test
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Alice"

def test_update_patient(client):
    # Setup
    payload = {"name": "Bob", "phone_number": "+444555666"}
    setup_resp = client.post("/patients/", json=payload).json()
    patient_id = setup_resp["patient_id"]

    # Test update
    update_payload = {"name": "Robert", "email": "robert@example.com", "age": 35}
    response = client.put(f"/patients/{patient_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Robert"
    assert response.json()["email"] == "robert@example.com"
    assert response.json()["age"] == 35

def test_delete_patient(client):
    # Setup
    payload = {"name": "Dave", "phone_number": "+777888999"}
    setup_resp = client.post("/patients/", json=payload).json()
    patient_id = setup_resp["patient_id"]

    # Test delete
    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify 404
    get_response = client.get(f"/patients/{patient_id}")
    get_response.status_code == status.HTTP_404_NOT_FOUND
