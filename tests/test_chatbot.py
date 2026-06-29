import json
from fastapi import status
from datetime import datetime

def test_chatbot_simple_chat(client, mock_ollama):
    mock_ollama["chat"].return_value = "Hello! Welcome to our fitness center. I can show you our membership plans."
    
    payload = {
        "session_id": "test_gym_session_1",
        "message": "Hi, who are you?"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["session_id"] == "test_gym_session_1"
    assert "membership plans" in data["response"]

def test_chatbot_history_maintenance(client, mock_ollama):
    session_id = "test_gym_session_2"
    mock_ollama["chat"].return_value = "Mock bot reply"

    # Send first message
    client.post("/chatbot/chat", json={"session_id": session_id, "message": "First message"})
    # Send second message
    client.post("/chatbot/chat", json={"session_id": session_id, "message": "Second message"})

    # Fetch history
    history_resp = client.get(f"/chatbot/history/{session_id}")
    assert history_resp.status_code == status.HTTP_200_OK
    history_data = history_resp.json()
    assert len(history_data["messages"]) == 4
    assert history_data["messages"][0]["message"] == "First message"
    assert history_data["messages"][1]["message"] == "Mock bot reply"

def test_chatbot_member_identify(client, mock_ollama):
    mock_ollama["chat"].return_value = """Hello Rahul! I've identified you.
```MEMBER_IDENTIFY
{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}
```"""

    payload = {
        "session_id": "test_gym_ident",
        "message": "My name is Rahul Kumar and phone is +919876543210"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "MEMBER_IDENTIFY" not in data["response"]
    assert data["member_id"] is not None

    # Check database
    member_id = data["member_id"]
    member_resp = client.get(f"/members/{member_id}")
    assert member_resp.status_code == status.HTTP_200_OK
    assert member_resp.json()["name"] == "Rahul Kumar"
    assert member_resp.json()["phone_number"] == "+919876543210"

def test_chatbot_membership_register(client, mock_ollama):
    # First seed membership plans in mock DB so we can reference them if needed
    plan_payload = {
        "plan_name": "Gold Membership",
        "duration": "12 Months",
        "price": 18000.00,
        "benefits": "Unlimited Gym Access",
        "description": "Premium pass"
    }
    client.post("/plans/", json=plan_payload)

    mock_ollama["chat"].return_value = """You are now registered for the Gold Membership!
```MEMBERSHIP_REGISTER
{
  "name": "Rahul Kumar",
  "phone": "+919876543210",
  "email": "rahul@gmail.com",
  "age": 24,
  "membership_plan": "Gold Membership"
}
```"""

    payload = {
        "session_id": "test_gym_reg",
        "message": "Register me for Gold Membership, my email is rahul@gmail.com and age is 24."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "MEMBERSHIP_REGISTER" not in data["response"]
    assert data["member_id"] is not None

    # Check member registration details
    member_id = data["member_id"]
    member_resp = client.get(f"/members/{member_id}")
    assert member_resp.status_code == status.HTTP_200_OK
    m_data = member_resp.json()
    assert m_data["email"] == "rahul@gmail.com"
    assert m_data["age"] == 24
    assert m_data["membership_status"] == "ACTIVE"

def test_chatbot_trainer_booking_confirm(client, mock_ollama):
    # Seed trainer
    trainer_payload = {
        "trainer_name": "Rahul Sharma",
        "specialization": "Weight Loss",
        "experience": "8 Years",
        "available_days": "Monday-Friday",
        "available_time": "6:00 AM - 2:00 PM",
        "session_fee": 600.00,
        "status": "ACTIVE"
    }
    t_resp = client.post("/trainers/", json=trainer_payload)
    assert t_resp.status_code == status.HTTP_201_CREATED

    mock_ollama["chat"].return_value = """I have booked your session with Rahul Sharma for tomorrow at 7 AM!
```TRAINER_BOOKING_CONFIRM
{
  "member_name": "Rahul Kumar",
  "phone": "+919876543210",
  "trainer_name": "Rahul Sharma",
  "booking_datetime": "2026-07-15 07:00:00",
  "training_goal": "Weight Loss"
}
```"""

    payload = {
        "session_id": "test_gym_booking",
        "message": "Book a session with Rahul Sharma for July 15th, 2026 at 7 AM."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "TRAINER_BOOKING_CONFIRM" not in data["response"]
    assert data["member_id"] is not None

    # Check trainer bookings in DB
    bookings_resp = client.get("/trainer_bookings/")
    assert bookings_resp.status_code == status.HTTP_200_OK
    bookings = bookings_resp.json()
    assert len(bookings) == 1
    assert bookings[0]["training_goal"] == "Weight Loss"
    assert bookings[0]["status"] == "CONFIRMED"

def test_chatbot_trainer_booking_cancel(client, mock_ollama):
    # Seed member, trainer, booking
    member_payload = {"name": "Rahul Kumar", "phone_number": "+919876543210"}
    m_resp = client.post("/members/", json=member_payload)
    member_id = m_resp.json()["member_id"]

    trainer_payload = {
        "trainer_name": "Rahul Sharma",
        "specialization": "Weight Loss",
        "experience": "8 Years",
        "available_days": "Monday-Friday",
        "available_time": "6:00 AM - 2:00 PM",
        "session_fee": 600.00,
        "status": "ACTIVE"
    }
    t_resp = client.post("/trainers/", json=trainer_payload)
    trainer_id = t_resp.json()["trainer_id"]

    booking_payload = {
        "member_id": member_id,
        "trainer_id": trainer_id,
        "booking_datetime": "2026-07-15T07:00:00",
        "status": "CONFIRMED",
        "training_goal": "Weight Loss"
    }
    b_resp = client.post("/trainer_bookings/", json=booking_payload)
    booking_id = b_resp.json()["booking_id"]

    mock_ollama["chat"].return_value = f"""I've cancelled your booking #{booking_id}.
```TRAINER_BOOKING_CANCEL
{{
  "booking_id": {booking_id}
}}
```"""

    payload = {
        "session_id": "test_gym_cancel",
        "message": f"Cancel my booking #{booking_id}"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "TRAINER_BOOKING_CANCEL" not in data["response"]

    # Verify booking status is now CANCELLED
    check_resp = client.get(f"/trainer_bookings/{booking_id}")
    assert check_resp.status_code == status.HTTP_200_OK
    assert check_resp.json()["status"] == "CANCELLED"
