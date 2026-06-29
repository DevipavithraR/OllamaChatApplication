import json
from fastapi import status

def test_chatbot_simple_chat(client, mock_ollama):
    mock_ollama["chat"].return_value = "Hello! Welcome to our college. How can I help you today?"
    
    payload = {
        "session_id": "test_session_1",
        "message": "Hi, who are you?"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["session_id"] == "test_session_1"
    assert data["response"] == "Hello! Welcome to our college. How can I help you today?"

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

def test_chatbot_action_tag_student_identify(client, mock_ollama):
    mock_ollama["chat"].return_value = """I have verified your details, Rahul Kumar. How can I help you?
```STUDENT_IDENTIFY
{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}
```"""

    payload = {
        "session_id": "test_identify_session",
        "message": "I am Rahul Kumar, my phone is +919876543210."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert "STUDENT_IDENTIFY" not in data["response"]
    assert "Rahul Kumar" in data["response"]
    assert data["student_id"] is not None

    # Verify that the student was created in the database
    s_id = data["student_id"]
    s_resp = client.get(f"/students/{s_id}")
    assert s_resp.status_code == status.HTTP_200_OK
    assert s_resp.json()["name"] == "Rahul Kumar"
    assert s_resp.json()["phone_number"] == "+919876543210"

def test_chatbot_action_tag_admission_apply(client, mock_ollama):
    # Setup Department & Course in DB
    dept = client.post("/departments/", json={
        "department_name": "Computer Science Department",
        "description": "CS Focuses on AI"
    }).json()
    
    client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept["department_id"],
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    })

    # Set mock Ollama response with application block
    mock_ollama["chat"].return_value = """I have submitted your application for B.Tech Computer Science!
```ADMISSION_APPLY
{
  "name": "Rahul Kumar",
  "phone": "+919876543210",
  "email": "rahul@gmail.com",
  "course": "B.Tech Computer Science",
  "marks_percentage": 82,
  "application_date": "2026-07-02"
}
```"""

    payload = {
        "session_id": "test_apply_session",
        "message": "Apply me for B.Tech CS, my email is rahul@gmail.com, name is Rahul Kumar, phone is +919876543210 and marks 82."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "ADMISSION_APPLY" not in data["response"]
    assert data["student_id"] is not None

    # Verify admission exists in DB
    adm_resp = client.get("/admissions/")
    assert adm_resp.status_code == status.HTTP_200_OK
    adm_data = adm_resp.json()
    assert len(adm_data) == 1
    assert adm_data[0]["status"] == "Pending Verification"
    assert adm_data[0]["course"]["course_name"] == "B.Tech Computer Science"

def test_chatbot_action_tag_admission_status(client, mock_ollama):
    # Setup Student, Dept, Course, Admission
    s = client.post("/students/", json={"name": "Rahul Kumar", "phone_number": "+919876543210"}).json()
    dept = client.post("/departments/", json={"department_name": "CS Department"}).json()
    c = client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept["department_id"],
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    }).json()
    adm = client.post("/admissions/", json={
        "student_id": s["student_id"],
        "course_id": c["course_id"],
        "application_date": "2026-07-02"
    }).json()

    adm_id = adm["admission_id"]

    # Set mock response for status inquiry
    mock_ollama["chat"].return_value = f"""Here is your application status details.
```ADMISSION_STATUS
{{
  "application_id": {adm_id}
}}
```"""

    payload = {
        "session_id": "test_status_session",
        "message": f"Check status of my application #{adm_id}"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    res_text = response.json()["response"]
    assert "ADMISSION_STATUS" not in res_text
    assert f"Application Status for #{adm_id}" in res_text
    assert "Pending Verification" in res_text

def test_chatbot_action_tag_admission_cancellation(client, mock_ollama):
    # Setup Student, Dept, Course, Admission
    s = client.post("/students/", json={"name": "Rahul Kumar", "phone_number": "+919876543210"}).json()
    dept = client.post("/departments/", json={"department_name": "CS Department"}).json()
    c = client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept["department_id"],
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    }).json()
    adm = client.post("/admissions/", json={
        "student_id": s["student_id"],
        "course_id": c["course_id"],
        "application_date": "2026-07-02"
    }).json()

    adm_id = adm["admission_id"]

    # Set mock response for cancellation
    mock_ollama["chat"].return_value = f"""Sure, I have cancelled your application.
```APPLICATION_CANCEL
{{
  "application_id": {adm_id}
}}
```"""

    payload = {
        "session_id": "test_cancel_session",
        "message": f"Cancel my application #{adm_id}"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert "APPLICATION_CANCEL" not in response.json()["response"]

    # Verify admission is cancelled
    get_adm = client.get(f"/admissions/{adm_id}")
    assert get_adm.json()["status"] == "Cancelled"
