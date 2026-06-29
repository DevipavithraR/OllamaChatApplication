from datetime import datetime
from typing import List, Optional
from app.models.book import Book
from app.models.member import Member
from app.models.issued_book import IssuedBook

class PromptBuilder:
    @staticmethod
    def build_system_prompt(
        books: List[Book], 
        member: Optional[Member] = None, 
        issued_records: List[IssuedBook] = None
    ) -> str:
        # Build Book Context
        if books:
            book_lines = []
            for b in books:
                status_str = "Available" if b.available_copies > 0 else "Out of Stock"
                book_lines.append(
                    f"- Title: {b.title}\n"
                    f"  Author: {b.author}\n"
                    f"  Category: {b.category}\n"
                    f"  ISBN: {b.isbn}\n"
                    f"  Publisher: {b.publisher}\n"
                    f"  Publication Year: {b.publication_year}\n"
                    f"  Available Copies: {b.available_copies}\n"
                    f"  Total Copies: {b.total_copies}\n"
                    f"  Status: {status_str}\n"
                    f"  Description: {b.description or 'N/A'}"
                )
            book_context = "\n".join(book_lines)
        else:
            book_context = "No matching book records found in the database search."

        # Build Member Context
        if member:
            member_context = (
                f"Identified Member: {member.name}\n"
                f"Phone: {member.phone_number}\n"
                f"Email: {member.email or 'N/A'}\n"
                f"Membership Type: {member.membership_type}\n"
                f"Member ID: {member.member_id}"
            )
        else:
            member_context = "Anonymous Member (Not logged in / identified yet)"

        # Build Borrowing History Context
        if member and issued_records:
            record_lines = []
            for r in issued_records:
                ret_date = r.return_date.strftime("%Y-%m-%d") if r.return_date else "N/A"
                record_lines.append(
                    f"- Issue ID {r.issue_id}: Book '{r.book.title}' (Book ID: {r.book_id})\n"
                    f"  Issue Date: {r.issue_date.strftime('%Y-%m-%d')}\n"
                    f"  Due Date: {r.due_date.strftime('%Y-%m-%d')}\n"
                    f"  Return Date: {ret_date}\n"
                    f"  Status: {r.status}"
                )
            issued_context = "\n".join(record_lines)
        else:
            issued_context = "No borrowing history or active issued books found for this member."

        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        system_prompt = f"""You are the Digital Library Assistant for our AI-powered library.
Your goal is to assist members in searching books, showing availability, registering members, issuing/returning books, checking due dates, and viewing history.

CRITICAL RULES (No Hallucination Policy):
1. You MUST ONLY answer library questions using the provided "Book Context", "Member Context", and "Issued Books Context" below.
2. If the user asks about books, authors, availability, due dates, ISBNs, or records not present in the context, you MUST reply:
   "I'm sorry. That information is not available in the library database."
3. Never invent book titles, authors, availability, due dates, ISBN numbers, or library policies.
4. Keep your answers concise, helpful, and professional.
5. Assume the current date and time is: {current_time_str}.

---
CONTEXT FROM LIBRARY DATABASE
---

[Book Context]
{book_context}

[Member Context]
{member_context}

[Issued Books Context]
{issued_context}

---
STRUCTURED OUTPUT TAGS & ACTIONS
---
You communicate database operations via JSON tags at the very end of your response inside triple backticks:

1. MEMBER_IDENTIFY
If the user identifies themselves with Name and Phone Number, output:
```MEMBER_IDENTIFY
{{
  "name": "Rahul Kumar",
  "phone": "+919876543210"
}}
```

2. BOOK_ISSUE
When issuing a book, you must gather Member Name, Phone Number, and Book Title. Once collected, output:
```BOOK_ISSUE
{{
  "name": "Rahul Kumar",
  "phone": "+919876543210",
  "book_title": "Clean Code",
  "issue_date": "2026-07-05",
  "due_date": "2026-07-19"
}}
```
Note: Convert relative dates (e.g. "tomorrow", "next week") to absolute YYYY-MM-DD format using current date context. If the user does not specify dates, set the issue_date to today ({current_time_str[:10]}) and the due_date to exactly 14 days later.

3. BOOK_RETURN
When a user wants to return a book, identify the issue record from their "Issued Books Context" and output:
```BOOK_RETURN
{{
  "issue_id": 12
}}
```

4. DUE_DATE_CHECK
When checking due dates for a book, find the active issue record in the "Issued Books Context" and output:
```DUE_DATE_CHECK
{{
  "issue_id": 12
}}
```

Do not output these tags unless you have verified the necessary details from the user. Only append one JSON tag block per response.
"""
        return system_prompt
