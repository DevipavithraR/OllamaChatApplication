import json
from fastapi import status

def test_chatbot_simple_chat(client, mock_ollama):
    mock_ollama["chat"].return_value = "Hello! Welcome to Bella Italia. I can show you the menu."
    
    payload = {
        "session_id": "test_session_1",
        "message": "Hi, who are you?"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["session_id"] == "test_session_1"
    assert data["response"] == "Hello! Welcome to Bella Italia. I can show you the menu."

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
    assert history_data["messages"][0]["content"] == "First message"
    assert history_data["messages"][1]["content"] == "Mock bot reply"

def test_chatbot_action_tag_booking(client, mock_ollama):
    # Set the mock Ollama return value to output the special RESERVATION_CONFIRM code block
    mock_ollama["chat"].return_value = """I have booked your table successfully, Tommy Vercetti! See you then!
```RESERVATION_CONFIRM:
{
  "name": "Tommy Vercetti",
  "phone": "+1909808707",
  "datetime": "2026-07-25 20:00:00",
  "party_size": 3,
  "special_requests": "Quiet table near the back"
}
```"""

    payload = {
        "session_id": "test_booking_session",
        "message": "I want to book a table for 3 people under Tommy Vercetti, phone +1909808707, for July 25th at 8 PM."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # The JSON tag must be stripped from the final text response presented to the user
    assert "RESERVATION_CONFIRM" not in data["response"]
    assert "Tommy Vercetti" in data["response"]
    assert data["customer_id"] is not None

    # Verify that the customer was created in the database
    cust_id = data["customer_id"]
    cust_resp = client.get(f"/customers/{cust_id}")
    assert cust_resp.status_code == status.HTTP_200_OK
    assert cust_resp.json()["name"] == "Tommy Vercetti"
    assert cust_resp.json()["phone"] == "+1909808707"

    # Verify that the reservation was booked in the database
    res_resp = client.get("/reservations/customer/+1909808707")
    assert res_resp.status_code == status.HTTP_200_OK
    res_data = res_resp.json()
    assert len(res_data) == 1
    assert res_data[0]["party_size"] == 3
    assert res_data[0]["special_requests"] == "Quiet table near the back"
