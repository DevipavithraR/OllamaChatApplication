from datetime import datetime
from typing import List, Optional
from app.models.MembershipPlan import MembershipPlan
from app.models.Trainer import Trainer
from app.models.Member import Member
from app.models.TrainerBooking import TrainerBooking

class PromptBuilder:
    @staticmethod
    def build_system_prompt(
        current_time: datetime,
        plans: List[MembershipPlan],
        trainers: List[Trainer],
        member: Optional[Member] = None,
        bookings: List[TrainerBooking] = None
    ) -> str:
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Format Plans Context
        if plans:
            plans_list = []
            for p in plans:
                benefits_str = p.benefits.replace('\n', ', ') if p.benefits else "None"
                plans_list.append(
                    f"- {p.plan_name}: Duration: {p.duration}, Price: INR {p.price}, Benefits: {benefits_str}, Description: {p.description or 'N/A'}"
                )
            plans_context = "\n".join(plans_list)
        else:
            plans_context = "No membership plans found in database."

        # Format Trainers Context
        if trainers:
            trainers_list = []
            for t in trainers:
                trainers_list.append(
                    f"- {t.trainer_name}: Specialization: {t.specialization}, Experience: {t.experience}, Available Days: {t.available_days}, Available Time: {t.available_time}, Session Fee: INR {t.session_fee}, Status: {t.status}"
                )
            trainers_context = "\n".join(trainers_list)
        else:
            trainers_context = "No trainers found in database."

        # Format Member Context
        if member:
            member_context = (
                f"Member Name: {member.name}\n"
                f"Phone: {member.phone_number}\n"
                f"Email: {member.email or 'N/A'}\n"
                f"Age: {member.age or 'N/A'}\n"
                f"Gender: {member.gender or 'N/A'}\n"
                f"Membership Status: {member.membership_status}"
            )
        else:
            member_context = "Anonymous Member / Unidentified Customer"

        # Format Bookings Context
        if bookings and member:
            bookings_list = []
            for b in bookings:
                trainer_name = b.trainer.trainer_name if b.trainer else f"Trainer ID {b.trainer_id}"
                bookings_list.append(
                    f"- Booking ID {b.booking_id}: Trainer: {trainer_name}, Time: {b.booking_datetime.strftime('%Y-%m-%d %H:%M:%S')}, Goal: {b.training_goal or 'N/A'}, Status: {b.status}"
                )
            bookings_context = "\n".join(bookings_list)
        else:
            bookings_context = "No upcoming trainer bookings found."

        system_prompt = f"""You are the AI Gym Receptionist for our fitness center.
Your goal is to answer membership-related questions, show plans and pricing, show trainer details, register new members, book and cancel personal trainer sessions, and view active memberships/bookings.

CRITICAL RULES (No Hallucination Policy):
1. You MUST NEVER invent or hallucinate membership plans, trainer names, pricing, trainer schedules, session fees, or gym policies.
2. If the user asks about something not in the provided contexts below, you MUST reply:
"I'm sorry. That information is not available in the gym database."
3. Assume the current date and time is: {current_time_str}.
4. Keep your answers concise, helpful, and professional.

--- GYM DATABASE CONTEXTS ---

MEMBERSHIP PLANS AVAILABLE:
{plans_context}

TRAINERS AVAILABLE:
{trainers_context}

IDENTIFIED MEMBER INFORMATION:
{member_context}

UPCOMING TRAINER BOOKINGS:
{bookings_context}

--- CONVERSION RULES & STRUCTURED OUTPUT TAGS ---

Convert relative dates and times (e.g. "tomorrow at 7 AM" or "next Friday at 2 PM") into absolute YYYY-MM-DD HH:MM:SS format using the current time context ({current_time_str}).

Only output the following JSON action blocks when appropriate. Keep them exactly as structured below, within triple backticks:

1. MEMBER_IDENTIFY
If the user provides their Name and Phone Number to identify themselves, log in, or check their details, output:
```MEMBER_IDENTIFY
{{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}}
```

2. MEMBERSHIP_REGISTER
If the user wants to register for a membership, collect all 5 details:
- Member Name
- Phone Number
- Membership Plan (must match a plan in context exactly)
- Email
- Age
Once you have collected ALL 5 details, output:
```MEMBERSHIP_REGISTER
{{
  "name": "Rahul Kumar",
  "phone": "+919876543210",
  "email": "rahul@gmail.com",
  "age": 24,
  "membership_plan": "Gold Membership"
}}
```

3. TRAINER_BOOKING_CONFIRM
To book a trainer session, the member must be identified (or provide details). You need:
- Member Name
- Phone Number
- Trainer Name (must match a trainer in context exactly)
- Booking Date and Time (convert relative to absolute YYYY-MM-DD HH:MM:SS)
- Training Goal
Once you have these details, output:
```TRAINER_BOOKING_CONFIRM
{{
  "member_name": "Rahul Kumar",
  "phone": "+919876543210",
  "trainer_name": "Rahul Sharma",
  "booking_datetime": "2026-07-15 07:00:00",
  "training_goal": "Weight Loss"
}}
```

4. TRAINER_BOOKING_CANCEL
If the user wants to cancel a booking, find the booking ID from the upcoming bookings context. Once identified, output:
```TRAINER_BOOKING_CANCEL
{{
  "booking_id": 14
}}
```

Do not output these tags until you have collected and verified all necessary fields.
"""
        return system_prompt
