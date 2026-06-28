from fastapi import status

def test_create_doctor(client):
    payload = {
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM",
        "status": "ACTIVE"
    }
    response = client.post("/doctors/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Dr. Priya"
    assert data["specialization"] == "Cardiologist"
    assert "doctor_id" in data

def test_search_doctors(client):
    # Setup - insert doctors
    client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    })
    client.post("/doctors/", json={
        "name": "Dr. Sharma",
        "department": "Pediatrics",
        "specialization": "Pediatrician",
        "experience": 8,
        "consultation_fee": 500.00,
        "available_days": "Monday-Saturday",
        "available_time": "9 AM-1 PM"
    })

    # Search by specialization
    response = client.get("/doctors/search?q=Cardiologist")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Dr. Priya"

    # Search by name
    response = client.get("/doctors/search?q=Sharma")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["specialization"] == "Pediatrician"
