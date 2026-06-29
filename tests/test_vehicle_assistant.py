import json
from datetime import datetime
from fastapi import status
from app.models.Customer import Customer
from app.models.Vehicle import Vehicle
from app.models.Mechanic import Mechanic
from app.models.ServiceCatalog import ServiceCatalog
from app.models.ServiceBooking import ServiceBooking

def test_create_customer(client):
    payload = {
        "name": "Rahul Kumar",
        "phone_number": "+919876543210",
        "email": "rahul.kumar@example.com",
        "address": "123 Main St, Chennai"
    }
    response = client.post("/customers/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Rahul Kumar"
    assert data["phone_number"] == "+919876543210"
    assert "customer_id" in data

def test_create_vehicle(client):
    # Setup customer first
    cust_resp = client.post("/customers/", json={
        "name": "Rahul Kumar",
        "phone_number": "+919876543210"
    })
    customer_id = cust_resp.json()["customer_id"]

    payload = {
        "customer_id": customer_id,
        "vehicle_number": "TN69AB1234",
        "vehicle_brand": "Hyundai",
        "vehicle_model": "i20",
        "fuel_type": "Petrol",
        "manufacturing_year": 2023
    }
    response = client.post("/vehicles/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["vehicle_number"] == "TN69AB1234"
    assert data["vehicle_brand"] == "Hyundai"
    assert data["customer_id"] == customer_id

def test_service_catalog_search(client, db_session):
    # Seed services
    s1 = ServiceCatalog(service_name="General Service", description="Inspection and tuneup", estimated_duration="2 Hours", service_cost=2500.00)
    s2 = ServiceCatalog(service_name="Engine overhaul", description="Advanced mechanical work", estimated_duration="6 Hours", service_cost=8500.00)
    db_session.add_all([s1, s2])
    db_session.commit()

    # Get list
    response = client.get("/services/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_mechanic_search(client, db_session):
    # Seed mechanics
    m1 = Mechanic(name="Arun Kumar", specialization="Engine Repair", experience=10, available_status="Available")
    m2 = Mechanic(name="Rajesh Sharma", specialization="Brake Replacement", experience=8, available_status="Busy")
    db_session.add_all([m1, m2])
    db_session.commit()

    # Get list
    response = client.get("/mechanics/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_booking_creation_and_mechanic_assignment(client, db_session):
    # Seed customer, vehicle, service, and available mechanic
    c = Customer(name="Rahul Kumar", phone_number="+919876543210")
    db_session.add(c)
    db_session.flush()

    v = Vehicle(customer_id=c.customer_id, vehicle_number="TN69AB1234", vehicle_brand="Hyundai", vehicle_model="i20", fuel_type="Petrol", manufacturing_year=2023)
    db_session.add(v)

    s = ServiceCatalog(service_name="General Service", description="Inspection", estimated_duration="2 Hours", service_cost=2500.00)
    db_session.add(s)

    m = Mechanic(name="Senthil Kumar", specialization="General Service Specialist", experience=5, available_status="Available")
    db_session.add(m)
    db_session.commit()

    payload = {
        "customer_id": c.customer_id,
        "vehicle_id": v.vehicle_id,
        "service_id": s.service_id,
        "service_date": "2026-07-20T10:00:00",
        "booking_status": "Scheduled",
        "customer_notes": "Startup issues"
    }

    response = client.post("/service_bookings/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["booking_status"] == "Scheduled"
    assert data["mechanic_id"] == m.mechanic_id  # Automatically assigned
    assert data["estimated_completion"] is not None

def test_chatbot_identify_customer(client, mock_ollama, db_session):
    mock_ollama["chat"].return_value = """Sure, let me search for your profile in our system.
```CUSTOMER_IDENTIFY
{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}
```"""
    
    payload = {
        "session_id": "session_test_identify",
        "message": "Hi, I am Rahul Kumar, my phone number is +919876543210"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Assert tags stripped and customer logged
    assert "CUSTOMER_IDENTIFY" not in data["response"]
    assert data["customer_id"] is not None

    # Check database
    cust = db_session.query(Customer).filter(Customer.phone_number == "+919876543210").first()
    assert cust is not None
    assert cust.name == "Rahul Kumar"

def test_chatbot_register_vehicle(client, mock_ollama, db_session):
    mock_ollama["chat"].return_value = """Okay, I have registered your car!
```VEHICLE_REGISTER
{
  "customer_name": "Rahul Kumar",
  "phone": "+919876543210",
  "vehicle_number": "TN69AB1234",
  "vehicle_brand": "Hyundai",
  "vehicle_model": "i20",
  "fuel_type": "Petrol",
  "manufacturing_year": 2023
}
```"""

    payload = {
        "session_id": "session_test_vehicle",
        "message": "Please register my Hyundai i20 (TN69AB1234, Petrol, 2023) under Rahul Kumar, phone +919876543210"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "VEHICLE_REGISTER" not in data["response"]
    assert data["customer_id"] is not None

    # Verify in DB
    v = db_session.query(Vehicle).filter(Vehicle.vehicle_number == "TN69AB1234").first()
    assert v is not None
    assert v.vehicle_brand == "Hyundai"
    assert v.vehicle_model == "i20"

def test_chatbot_confirm_booking(client, mock_ollama, db_session):
    # Seed service and mechanic
    s = ServiceCatalog(service_name="General Service", description="Inspection", estimated_duration="2 Hours", service_cost=2500.00)
    db_session.add(s)
    m = Mechanic(name="Senthil Kumar", specialization="General Service", experience=5, available_status="Available")
    db_session.add(m)
    db_session.commit()

    mock_ollama["chat"].return_value = """I have booked your General Service!
```SERVICE_BOOKING_CONFIRM
{
  "customer_name": "Rahul Kumar",
  "phone": "+919876543210",
  "vehicle_number": "TN69AB1234",
  "service_name": "General Service",
  "service_date": "2026-07-20 10:00:00",
  "customer_notes": "Engine noise during startup"
}
```"""

    payload = {
        "session_id": "session_test_booking",
        "message": "Confirm booking for General Service, TN69AB1234, July 20th at 10 AM, Rahul, +919876543210"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "SERVICE_BOOKING_CONFIRM" not in data["response"]
    assert data["customer_id"] is not None

    # Verify booking in DB
    bk = db_session.query(ServiceBooking).first()
    assert bk is not None
    assert bk.service_id == s.service_id
    assert bk.mechanic_id == m.mechanic_id

def test_chatbot_track_status(client, mock_ollama, db_session):
    # Seed customer, vehicle, service, and booking
    c = Customer(name="Rahul Kumar", phone_number="+919876543210")
    db_session.add(c)
    db_session.flush()

    v = Vehicle(customer_id=c.customer_id, vehicle_number="TN69AB1234", vehicle_brand="Hyundai", vehicle_model="i20", fuel_type="Petrol", manufacturing_year=2023)
    db_session.add(v)

    s = ServiceCatalog(service_name="General Service", description="Inspection", estimated_duration="2 Hours", service_cost=2500.00)
    db_session.add(s)
    db_session.flush()

    bk = ServiceBooking(customer_id=c.customer_id, vehicle_id=v.vehicle_id, service_id=s.service_id, service_date=datetime(2026, 7, 20, 10, 0, 0), booking_status="In Progress")
    db_session.add(bk)
    db_session.commit()

    mock_ollama["chat"].return_value = f"""Checking status of booking {bk.booking_id}. It is currently In Progress.
```SERVICE_STATUS
{{
  "booking_id": {bk.booking_id}
}}
```"""

    payload = {
        "session_id": "session_test_status",
        "message": f"Track status of booking {bk.booking_id}"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "SERVICE_STATUS" not in data["response"]
    assert data["customer_id"] == c.customer_id

def test_chatbot_cancel_booking(client, mock_ollama, db_session):
    # Seed customer, vehicle, service, and booking
    c = Customer(name="Rahul Kumar", phone_number="+919876543210")
    db_session.add(c)
    db_session.flush()

    v = Vehicle(customer_id=c.customer_id, vehicle_number="TN69AB1234", vehicle_brand="Hyundai", vehicle_model="i20", fuel_type="Petrol", manufacturing_year=2023)
    db_session.add(v)

    s = ServiceCatalog(service_name="General Service", description="Inspection", estimated_duration="2 Hours", service_cost=2500.00)
    db_session.add(s)
    db_session.flush()

    bk = ServiceBooking(customer_id=c.customer_id, vehicle_id=v.vehicle_id, service_id=s.service_id, service_date=datetime(2026, 7, 20, 10, 0, 0), booking_status="Scheduled")
    db_session.add(bk)
    db_session.commit()

    mock_ollama["chat"].return_value = f"""Cancelling booking {bk.booking_id} as requested.
```SERVICE_CANCEL
{{
  "booking_id": {bk.booking_id}
}}
```"""

    payload = {
        "session_id": "session_test_cancel",
        "message": f"Cancel booking {bk.booking_id}"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "SERVICE_CANCEL" not in data["response"]

    # Verify status in DB is Cancelled
    db_session.refresh(bk)
    assert bk.booking_status == "Cancelled"

def test_conversation_history(client, mock_ollama):
    session_id = "session_history_test"
    mock_ollama["chat"].return_value = "Reply"

    client.post("/chatbot/chat", json={"session_id": session_id, "message": "Message 1"})
    client.post("/chatbot/chat", json={"session_id": session_id, "message": "Message 2"})

    response = client.get(f"/chatbot/history/{session_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["messages"]) == 4
    assert data["messages"][0]["message"] == "Message 1"
    assert data["messages"][1]["message"] == "Reply"
