import json
from fastapi import status

def test_chatbot_simple_chat(client, mock_ollama):
    mock_ollama["chat"].return_value = "Hello! Welcome to Cinema AI. I can help you book movie tickets."
    
    payload = {
        "session_id": "test_session_1",
        "message": "Hi, who are you?"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["session_id"] == "test_session_1"
    assert data["response"] == "Hello! Welcome to Cinema AI. I can help you book movie tickets."

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

def test_chatbot_action_tag_booking(client, mock_ollama):
    # Setup movie, theatre, show
    movie = client.post("/movies", json={
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "language": "English",
        "duration": "169 min",
        "rating": "PG-13"
    }).json()

    theatre = client.post("/theatres", json={
        "theatre_name": "PVR Cinemas",
        "location": "Mall of India",
        "screens": 4
    }).json()

    show = client.post("/shows", json={
        "movie_id": movie["movie_id"],
        "theatre_id": theatre["theatre_id"],
        "screen_number": 2,
        "show_datetime": "2026-07-20T19:30:00",
        "ticket_price": 250.0,
        "available_seats": 50,
        "total_seats": 50
    }).json()

    # Set mock Ollama return value to output the special MOVIE_BOOKING_CONFIRM code block
    mock_ollama["chat"].return_value = f"""I have booked your tickets successfully, Tommy! See you at the movies!
```MOVIE_BOOKING_CONFIRM:
{{
  "name": "Tommy Vercetti",
  "phone": "+1909808707",
  "show_id": {show['show_id']},
  "seat_numbers": ["A10", "A11"],
  "number_of_tickets": 2
}}
```"""

    payload = {
        "session_id": "test_booking_session",
        "message": f"I want to book 2 tickets for Interstellar show {show['show_id']} under Tommy Vercetti, phone +1909808707."
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # The JSON tag must be stripped from the final text response presented to the user
    assert "MOVIE_BOOKING_CONFIRM" not in data["response"]
    assert "Tommy" in data["response"]
    assert data["customer_id"] is not None

    # Verify that the customer was created in the database
    cust_id = data["customer_id"]
    cust_resp = client.get(f"/customers/{cust_id}")
    assert cust_resp.status_code == status.HTTP_200_OK
    assert cust_resp.json()["name"] == "Tommy Vercetti"
    assert cust_resp.json()["phone_number"] == "+1909808707"

    # Verify that the booking was recorded in the database
    book_resp = client.get(f"/bookings/customer/{cust_id}")
    assert book_resp.status_code == status.HTTP_200_OK
    book_data = book_resp.json()
    assert len(book_data) == 1
    assert book_data[0]["number_of_tickets"] == 2
    assert "A10, A11" in book_data[0]["seat_numbers"]
