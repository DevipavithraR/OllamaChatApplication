from fastapi import status

def test_create_reservation(client):
    # Setup Customer
    customer = client.post("/customers/", json={
        "name": "David",
        "phone": "+100200300"
    }).json()
    
    # Test Create Reservation
    payload = {
        "customer_id": customer["id"],
        "reservation_time": "2026-08-01T19:00:00",
        "party_size": 4,
        "special_requests": "Window seat"
    }
    response = client.post("/reservations/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["customer_id"] == customer["id"]
    assert data["party_size"] == 4
    assert data["status"] == "CONFIRMED"

def test_create_reservation_with_customer(client):
    payload = {
        "customer_name": "Edward",
        "customer_phone": "+400500600",
        "customer_email": "edward@example.com",
        "reservation_time": "2026-08-05T20:00:00",
        "party_size": 2
    }
    response = client.post("/reservations/with-customer", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["party_size"] == 2
    
    # Verify Customer was created behind the scenes
    customer_id = data["customer_id"]
    cust_response = client.get(f"/customers/{customer_id}")
    assert cust_response.status_code == status.HTTP_200_OK
    assert cust_response.json()["name"] == "Edward"
    assert cust_response.json()["phone"] == "+400500600"

def test_get_reservations_by_phone(client):
    # Setup reservation
    payload = {
        "customer_name": "Fiona",
        "customer_phone": "+700800900",
        "reservation_time": "2026-08-10T18:30:00",
        "party_size": 6
    }
    client.post("/reservations/with-customer", json=payload)

    # Query by phone
    response = client.get("/reservations/customer/+700800900")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["party_size"] == 6
