from fastapi import status

def test_booking_flow(client):
    # Setup customer, movie, theatre, show
    customer = client.post("/customers", json={
        "name": "Jane",
        "phone_number": "+1122",
        "email": "jane@example.com"
    }).json()

    movie = client.post("/movies", json={
        "title": "The Dark Knight",
        "genre": "Action",
        "language": "English",
        "duration": "152 min",
        "rating": "PG-13"
    }).json()

    theatre = client.post("/theatres", json={
        "theatre_name": "Wave Cinemas",
        "location": "Noida",
        "screens": 3
    }).json()

    show = client.post("/shows", json={
        "movie_id": movie["movie_id"],
        "theatre_id": theatre["theatre_id"],
        "screen_number": 2,
        "show_datetime": "2026-07-20T20:00:00",
        "ticket_price": 200.0,
        "available_seats": 50,
        "total_seats": 50
    }).json()

    # Test Create Booking
    payload = {
        "customer_id": customer["customer_id"],
        "show_id": show["show_id"],
        "seat_numbers": ["A1", "A2"],
        "number_of_tickets": 2,
        "total_amount": 400.0
    }
    res = client.post("/bookings", json=payload)
    assert res.status_code == status.HTTP_200_OK
    booking = res.json()
    assert booking["booking_status"] == "Confirmed"
    assert booking["number_of_tickets"] == 2
    assert "booking_id" in booking

    # Check Show seats decreased
    show_res = client.get(f"/shows/{show['show_id']}")
    assert show_res.json()["available_seats"] == 48

    # Test Booking Modification (change to 3 tickets)
    modify_payload = {
        "seat_numbers": ["A1", "A2", "A3"],
        "number_of_tickets": 3
    }
    mod_res = client.put(f"/bookings/{booking['booking_id']}", json=modify_payload)
    assert mod_res.status_code == status.HTTP_200_OK
    assert mod_res.json()["number_of_tickets"] == 3

    # Check Show seats decreased further
    show_res = client.get(f"/shows/{show['show_id']}")
    assert show_res.json()["available_seats"] == 47

    # Cancel Booking
    cancel_res = client.post(f"/bookings/{booking['booking_id']}/cancel")
    assert cancel_res.status_code == status.HTTP_200_OK
    assert cancel_res.json()["booking_status"] == "Cancelled"

    # Check Show seats restored
    show_res = client.get(f"/shows/{show['show_id']}")
    assert show_res.json()["available_seats"] == 50
