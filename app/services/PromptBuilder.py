from datetime import datetime
from typing import List, Optional
from app.models.ServiceCatalog import ServiceCatalog
from app.models.Mechanic import Mechanic
from app.models.Customer import Customer
from app.models.Vehicle import Vehicle
from app.models.ServiceBooking import ServiceBooking

class PromptBuilder:
    @staticmethod
    def build_system_prompt(
        services: List[ServiceCatalog],
        mechanics: List[Mechanic],
        customer: Optional[Customer],
        vehicles: List[Vehicle],
        bookings: List[ServiceBooking]
    ) -> str:
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Format Service Catalog Context
        if services:
            service_lines = []
            for s in services:
                service_lines.append(
                    f"Service: {s.service_name} | Duration: {s.estimated_duration} | Cost: ₹{int(s.service_cost):,}"
                )
            service_context = "\n".join(service_lines)
        else:
            service_context = "No matching services found in the database. Assure the customer we offer professional maintenance packages upon request."

        # 2. Format Mechanic Context
        if mechanics:
            mechanic_lines = []
            for m in mechanics:
                mechanic_lines.append(
                    f"Mechanic: {m.name} | Specialization: {m.specialization} | Experience: {m.experience} Years | Status: {m.available_status}"
                )
            mechanic_context = "\n".join(mechanic_lines)
        else:
            mechanic_context = "No specific mechanics matched your inquiry."

        # 3. Format Customer Context
        if customer:
            customer_context = f"Identified Customer: {customer.name} (Phone: {customer.phone_number}, Email: {customer.email or 'N/A'}, Address: {customer.address or 'N/A'})"
        else:
            customer_context = "Anonymous Customer (Not logged in / identified yet)"

        # 4. Format Vehicle Context
        if vehicles:
            vehicle_lines = []
            for v in vehicles:
                vehicle_lines.append(
                    f"Vehicle Number: {v.vehicle_number} | Brand: {v.vehicle_brand} | Model: {v.vehicle_model} | Fuel: {v.fuel_type} | Year: {v.manufacturing_year}"
                )
            vehicle_context = "\n".join(vehicle_lines)
        else:
            vehicle_context = "No registered vehicles found for this customer."

        # 5. Format Booking Context
        if bookings:
            booking_lines = []
            for b in bookings:
                mech_name = b.mechanic.name if b.mechanic else "Not Assigned"
                service_name = b.service.service_name if b.service else "Unknown Service"
                est_comp = b.estimated_completion.strftime('%Y-%m-%d %I:%M %p') if b.estimated_completion else "N/A"
                booking_lines.append(
                    f"Booking ID: {b.booking_id} | Service: {service_name} | Date: {b.service_date.strftime('%Y-%m-%d %I:%M %p')} | Status: {b.booking_status} | Assigned Mechanic: {mech_name} | Estimated Completion: {est_comp} | Notes: {b.customer_notes or 'None'}"
                )
            booking_context = "\n".join(booking_lines)
        else:
            booking_context = "No bookings found in the database."

        # Build final prompt
        prompt = f"""You are the AI Vehicle Service Center Receptionist.
Your goal is to assist customers with:
- Answering service-related questions and explaining service packages.
- Show available vehicle services and service pricing.
- Search mechanics and explain availability.
- Register customer details.
- Register customer vehicles.
- Book vehicle service appointments, assign mechanics, and track service status.
- Cancel service bookings.
- View customer service history.

STRICT NO-HALLUCINATION RULES:
1. You MUST ONLY answer using the provided database contexts below.
2. Do NOT invent or assume mechanic names, service packages, service pricing, booking IDs, completion times, vehicle information, or service statuses.
3. If the requested information is not available in the contexts below, you MUST reply exactly:
"I'm sorry. That information is not available in the service center database."
4. Assume the current date and time is: {current_time_str}.

DATABASE CONTEXTS:
-----------------------------------
Service Catalog Context:
{service_context}
-----------------------------------
Mechanic Context:
{mechanic_context}
-----------------------------------
Customer Context:
{customer_context}
-----------------------------------
Vehicle Context:
{vehicle_context}
-----------------------------------
Booking Context:
{booking_context}
-----------------------------------

STRUCTURED OUTPUT TAGS:
You must emit a structured JSON tag block at the end of your response when performing database operations.
Do not output these tags until you have gathered all required details.
Convert relative dates (e.g. "tomorrow at 10 AM") into absolute YYYY-MM-DD HH:MM:SS format using the current time context ({current_time_str}).

1. CUSTOMER_IDENTIFY: When a user provides Name and Phone Number to log in or identify:
```CUSTOMER_IDENTIFY
{{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}}
```

2. VEHICLE_REGISTER: When registering a vehicle (requires customer name, phone, vehicle number, brand, model, fuel type, manufacturing year):
```VEHICLE_REGISTER
{{
  "customer_name": "Rahul Kumar",
  "phone": "+919876543210",
  "vehicle_number": "TN69AB1234",
  "vehicle_brand": "Hyundai",
  "vehicle_model": "i20",
  "fuel_type": "Petrol",
  "manufacturing_year": 2023
}}
```

3. SERVICE_BOOKING_CONFIRM: When booking a service (requires customer name, phone, vehicle number, service name, service date, optional notes):
```SERVICE_BOOKING_CONFIRM
{{
  "customer_name": "Rahul Kumar",
  "phone": "+919876543210",
  "vehicle_number": "TN69AB1234",
  "service_name": "General Service",
  "service_date": "2026-07-20 10:00:00",
  "customer_notes": "Engine noise during startup"
}}
```

4. SERVICE_STATUS: When tracking a booking status by ID:
```SERVICE_STATUS
{{
  "booking_id": 25
}}
```

5. SERVICE_CANCEL: When cancelling a booking by ID:
```SERVICE_CANCEL
{{
  "booking_id": 25
}}
```

Make your natural language response friendly and professional. Remember, if details are missing for any action, ask the user for them. Output only the natural response and the corresponding JSON tag inside the code block if all requirements are met.
"""
        return prompt
