from fastapi import status

def test_book_appointment(client):
    # Setup Patient and Doctor
    patient = client.post("/patients/", json={
        "name": "Rahul",
        "phone_number": "+919876543210",
        "age": 28,
        "gender": "Male"
    }).json()
    
    doctor = client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    }).json()

    # Book Appointment
    payload = {
        "patient_id": patient["patient_id"],
        "doctor_id": doctor["doctor_id"],
        "appointment_datetime": "2026-07-05T11:30:00",
        "status": "CONFIRMED",
        "special_notes": "General checkup"
    }
    response = client.post("/appointments/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["patient_id"] == patient["patient_id"]
    assert data["doctor_id"] == doctor["doctor_id"]
    assert "appointment_id" in data
    assert data["status"] == "CONFIRMED"

def test_reschedule_appointment(client):
    # Setup
    patient = client.post("/patients/", json={"name": "Rahul", "phone_number": "+919876543210"}).json()
    doctor = client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    }).json()
    
    appointment = client.post("/appointments/", json={
        "patient_id": patient["patient_id"],
        "doctor_id": doctor["doctor_id"],
        "appointment_datetime": "2026-07-05T11:30:00"
    }).json()

    # Test Reschedule
    app_id = appointment["appointment_id"]
    payload = {"appointment_datetime": "2026-07-08T15:30:00"}
    response = client.put(f"/appointments/{app_id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["appointment_datetime"].replace("Z", "") == "2026-07-08T15:30:00"

def test_cancel_appointment(client):
    # Setup
    patient = client.post("/patients/", json={"name": "Rahul", "phone_number": "+919876543210"}).json()
    doctor = client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    }).json()
    
    appointment = client.post("/appointments/", json={
        "patient_id": patient["patient_id"],
        "doctor_id": doctor["doctor_id"],
        "appointment_datetime": "2026-07-05T11:30:00"
    }).json()

    app_id = appointment["appointment_id"]
    # Delete test (matching frontend cancellation behavior)
    response = client.delete(f"/appointments/{app_id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify 404
    get_response = client.get(f"/appointments/{app_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
