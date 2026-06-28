import json
from fastapi import status

def test_chatbot_simple_chat(client, mock_ollama):
    mock_ollama["chat"].return_value = "Hello! Welcome to Hope Hospital. How can I help you today?"
    
    payload = {
        "session_id": "test_session_1",
        "message": "Hi, who are you?"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["session_id"] == "test_session_1"
    assert data["response"] == "Hello! Welcome to Hope Hospital. How can I help you today?"

def test_chatbot_history_maintenance(client, mock_ollama):
    session_id = "test_session_2"
    mock_ollama["chat"].return_value = "Mock bot reply"

    # Send first message
    client.post("/chatbot/chat", json={"session_id": session_id, "message": "First message"})
    # Send second message
    client.post("/chatbot/chat", json={"session_id": session_id, "message": "Second message"})

    # Fetch history
    history_resp = client.get(f"/chatbot/history/{session_id}")
    assert history_resp.status_code == status.HTTP_200_OK
    history_data = history_resp.json()
    assert len(history_data["messages"]) == 4  # (User -> Bot -> User -> Bot)
    assert history_data["messages"][0]["message"] == "First message"
    assert history_data["messages"][1]["message"] == "Mock bot reply"

def test_chatbot_action_tag_patient_identify(client, mock_ollama):
    # Set the mock Ollama return value to output the special PATIENT_IDENTIFY code block
    mock_ollama["chat"].return_value = """I have verified your patient details, Rahul. How can I help you?
```PATIENT_IDENTIFY
{
  "name": "Rahul",
  "phone": "+919876543210"
}
```"""

    payload = {
        "session_id": "test_identify_session",
        "message": "I am Rahul, my phone is +919876543210."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert "PATIENT_IDENTIFY" not in data["response"]
    assert "Rahul" in data["response"]
    assert data["patient_id"] is not None

    # Verify that the patient was created in the database
    p_id = data["patient_id"]
    p_resp = client.get(f"/patients/{p_id}")
    assert p_resp.status_code == status.HTTP_200_OK
    assert p_resp.json()["name"] == "Rahul"
    assert p_resp.json()["phone_number"] == "+919876543210"

def test_chatbot_action_tag_appointment_booking(client, mock_ollama):
    # Setup Doctor in DB
    client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    })

    # Set mock Ollama response with booking block
    mock_ollama["chat"].return_value = """I have confirmed your appointment with Dr. Priya for July 5th at 11:30 AM!
```APPOINTMENT_CONFIRM
{
  "name": "Rahul",
  "phone": "+919876543210",
  "doctor": "Dr. Priya",
  "appointment_datetime": "2026-07-05 11:30:00",
  "department": "Cardiology",
  "special_notes": "General checkup"
}
```"""

    payload = {
        "session_id": "test_booking_session",
        "message": "Book me an appointment with Dr. Priya tomorrow at 11:30 AM."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "APPOINTMENT_CONFIRM" not in data["response"]
    assert data["patient_id"] is not None

    # Verify appointment exists in DB
    app_resp = client.get("/appointments/")
    assert app_resp.status_code == status.HTTP_200_OK
    app_data = app_resp.json()
    assert len(app_data) == 1
    assert app_data[0]["status"] == "CONFIRMED"
    assert app_data[0]["special_notes"] == "General checkup"

def test_chatbot_action_tag_appointment_cancellation(client, mock_ollama):
    # Setup Patient, Doctor, Appointment
    p = client.post("/patients/", json={"name": "Rahul", "phone_number": "+919876543210"}).json()
    d = client.post("/doctors/", json={
        "name": "Dr. Priya",
        "department": "Cardiology",
        "specialization": "Cardiologist",
        "experience": 12,
        "consultation_fee": 700.00,
        "available_days": "Monday-Friday",
        "available_time": "10 AM-4 PM"
    }).json()
    app = client.post("/appointments/", json={
        "patient_id": p["patient_id"],
        "doctor_id": d["doctor_id"],
        "appointment_datetime": "2026-07-05T11:30:00"
    }).json()

    app_id = app["appointment_id"]

    # Set mock response for cancellation
    mock_ollama["chat"].return_value = f"""Sure, I have cancelled your appointment with ID {app_id}.
```APPOINTMENT_CANCEL
{{
  "appointment_id": {app_id}
}}
```"""

    response = client.post("/chatbot/chat", json={"session_id": "test_cancel_session", "message": f"Cancel my appointment {app_id}."})
    assert response.status_code == status.HTTP_200_OK
    assert "APPOINTMENT_CANCEL" not in response.json()["response"]

    # Verify appointment is cancelled
    get_app = client.get(f"/appointments/{app_id}")
    assert get_app.json()["status"] == "CANCELLED"
