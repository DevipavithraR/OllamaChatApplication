import json
from datetime import date
from fastapi import status

# 1. Member Registration Tests
def test_member_registration(client):
    # Register a new member
    payload = {
        "name": "Jane Doe",
        "phone_number": "+1222333444",
        "email": "jane@example.com",
        "membership_type": "Premium"
    }
    response = client.post("/members/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["phone_number"] == "+1222333444"
    assert data["member_id"] is not None

    # Test duplicate registration error
    response_dup = client.post("/members/", json=payload)
    assert response_dup.status_code == status.HTTP_400_BAD_REQUEST

    # Get members list
    response_get = client.get("/members/")
    assert response_get.status_code == status.HTTP_200_OK
    members = response_get.json()
    assert len(members) == 1
    assert members[0]["name"] == "Jane Doe"


# 2. Book Search & Availability Tests
def test_book_search_availability(client):
    # Insert a book
    book_payload = {
        "title": "Test-Driven Development",
        "author": "Kent Beck",
        "category": "Programming",
        "isbn": "978-0321146533",
        "publisher": "Addison-Wesley",
        "publication_year": 2002,
        "available_copies": 3,
        "total_copies": 3,
        "description": "Write clean code that works."
    }
    response = client.post("/books/", json=book_payload)
    assert response.status_code == status.HTTP_201_CREATED
    book = response.json()
    assert book["book_id"] is not None

    # Search for book
    search_resp = client.get("/books/search?q=Driven")
    assert search_resp.status_code == status.HTTP_200_OK
    results = search_resp.json()
    assert len(results) == 1
    assert results[0]["title"] == "Test-Driven Development"


# 3. Book Issue & Return API Tests
def test_book_issue_and_return(client):
    # Create member
    member = client.post("/members/", json={
        "name": "Bob Smith",
        "phone_number": "+1444555666",
        "email": "bob@example.com",
        "membership_type": "Regular"
    }).json()

    # Create book
    book = client.post("/books/", json={
        "title": "Refactoring",
        "author": "Martin Fowler",
        "category": "Programming",
        "isbn": "978-0134757599",
        "publisher": "Addison-Wesley",
        "publication_year": 2018,
        "available_copies": 2,
        "total_copies": 2,
        "description": "Improving the design of existing code."
    }).json()

    # Issue book
    issue_payload = {
        "member_id": member["member_id"],
        "book_id": book["book_id"],
        "due_date": "2026-07-15"
    }
    issue_resp = client.post("/issued_books/", json=issue_payload)
    assert issue_resp.status_code == status.HTTP_201_CREATED
    issue = issue_resp.json()
    assert issue["status"] == "Issued"
    assert issue["book_title"] == "Refactoring"
    assert issue["member_name"] == "Bob Smith"

    # Verify book copies decreased
    book_after = client.get(f"/books/{book['book_id']}").json()
    assert book_after["available_copies"] == 1

    # Return book
    return_resp = client.put(f"/issued_books/{issue['issue_id']}")
    assert return_resp.status_code == status.HTTP_200_OK
    returned = return_resp.json()
    assert returned["status"] == "Returned"
    assert returned["return_date"] == date.today().strftime("%Y-%m-%d")

    # Verify book copies restored
    book_restored = client.get(f"/books/{book['book_id']}").json()
    assert book_restored["available_copies"] == 2


# 4. Chatbot Identify Interception Action
def test_chatbot_identify(client, mock_ollama):
    mock_ollama["chat"].return_value = """I have identified you! Welcome to the library.
```MEMBER_IDENTIFY
{
  "name": "Jane Doe",
  "phone": "+1999888777"
}
```"""

    payload = {
        "session_id": "session_ident_123",
        "message": "I am Jane Doe, phone +1999888777"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "MEMBER_IDENTIFY" not in data["response"]
    assert "identified you" in data["response"]
    assert data["member_id"] is not None

    # Verify member registered in DB
    member_id = data["member_id"]
    member_resp = client.get(f"/members/{member_id}")
    assert member_resp.status_code == status.HTTP_200_OK
    assert member_resp.json()["name"] == "Jane Doe"
    assert member_resp.json()["phone_number"] == "+1999888777"


# 5. Chatbot Book Issue Interception Action
def test_chatbot_issue(client, mock_ollama):
    # Pre-register member and book so issue can succeed
    member = client.post("/members/", json={
        "name": "Rahul Kumar",
        "phone_number": "+919876543210",
        "email": "rahul@example.com"
    }).json()

    book = client.post("/books/", json={
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming",
        "isbn": "978-0132350884",
        "publisher": "Prentice Hall",
        "publication_year": 2008,
        "available_copies": 5,
        "total_copies": 5
    }).json()

    mock_ollama["chat"].return_value = """I have successfully issued the book Clean Code to you!
```BOOK_ISSUE
{
  "name": "Rahul Kumar",
  "phone": "+919876543210",
  "book_title": "Clean Code",
  "issue_date": "2026-07-05",
  "due_date": "2026-07-19"
}
```"""

    payload = {
        "session_id": "session_issue_123",
        "message": "Issue Clean Code for Rahul Kumar"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "BOOK_ISSUE" not in data["response"]
    assert "successfully issued" in data["response"]

    # Verify book copies decreased
    book_after = client.get(f"/books/{book['book_id']}").json()
    assert book_after["available_copies"] == 4

    # Verify issue record exists
    issues = client.get("/issued_books/").json()
    assert len(issues) == 1
    assert issues[0]["book_title"] == "Clean Code"
    assert issues[0]["status"] == "Issued"


# 6. Chatbot Book Return Interception Action
def test_chatbot_return(client, mock_ollama):
    # Pre-register and issue a book
    member = client.post("/members/", json={
        "name": "Alice Smith",
        "phone_number": "+15550199",
        "email": "alice@example.com"
    }).json()

    book = client.post("/books/", json={
        "title": "Design Patterns",
        "author": "Erich Gamma",
        "category": "Programming",
        "isbn": "978-0201633610",
        "publisher": "Addison-Wesley",
        "publication_year": 1994,
        "available_copies": 2,
        "total_copies": 2
    }).json()

    issue = client.post("/issued_books/", json={
        "member_id": member["member_id"],
        "book_id": book["book_id"],
        "due_date": "2026-07-15"
    }).json()

    mock_ollama["chat"].return_value = f"""Thank you for returning the book! I have processed it.
```BOOK_RETURN
{{
  "issue_id": {issue['issue_id']}
}}
```"""

    payload = {
        "session_id": "session_return_123",
        "message": "I want to return Design Patterns"
    }
    response = client.post("/chatbot/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "BOOK_RETURN" not in data["response"]

    # Verify book copies restored
    book_after = client.get(f"/books/{book['book_id']}").json()
    assert book_after["available_copies"] == 2

    # Verify issue status updated
    issue_after = client.get(f"/issued_books/{issue['issue_id']}").json()
    assert issue_after["status"] == "Returned"
