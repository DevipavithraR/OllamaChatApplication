from fastapi import status

def test_create_student(client):
    payload = {
        "name": "Rahul",
        "phone_number": "+919876543210",
        "email": "rahul@example.com",
        "gender": "Male",
        "marks_percentage": 82.5
    }
    response = client.post("/students/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Rahul"
    assert data["phone_number"] == "+919876543210"
    assert "student_id" in data

def test_create_student_duplicate_phone(client):
    payload = {
        "name": "Rahul",
        "phone_number": "+919876543210",
        "email": "rahul@example.com",
        "gender": "Male",
        "marks_percentage": 82.5
    }
    # Create first student
    client.post("/students/", json=payload)
    
    # Attempt duplicate creation
    response = client.post("/students/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_get_student(client):
    # Setup
    payload = {"name": "Alice", "phone_number": "+111222333"}
    setup_resp = client.post("/students/", json=payload).json()
    student_id = setup_resp["student_id"]

    # Test
    response = client.get(f"/students/{student_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Alice"

def test_update_student(client):
    # Setup
    payload = {"name": "Bob", "phone_number": "+444555666"}
    setup_resp = client.post("/students/", json=payload).json()
    student_id = setup_resp["student_id"]

    # Test update
    update_payload = {"name": "Robert", "email": "robert@example.com", "marks_percentage": 91.0}
    response = client.put(f"/students/{student_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Robert"
    assert response.json()["email"] == "robert@example.com"
    assert response.json()["marks_percentage"] == 91.0

def test_delete_student(client):
    # Setup
    payload = {"name": "Dave", "phone_number": "+777888999"}
    setup_resp = client.post("/students/", json=payload).json()
    student_id = setup_resp["student_id"]

    # Test delete
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify 404
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
