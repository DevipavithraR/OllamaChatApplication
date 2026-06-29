from fastapi import status

def test_apply_admission(client):
    # Setup Student and Course
    student = client.post("/students/", json={
        "name": "Rahul",
        "phone_number": "+919876543210",
        "marks_percentage": 82.5
    }).json()
    
    dept = client.post("/departments/", json={
        "department_name": "Computer Science Department",
        "description": "CS description"
    }).json()

    course = client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept["department_id"],
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    }).json()

    # Apply Admission
    payload = {
        "student_id": student["student_id"],
        "course_id": course["course_id"],
        "application_date": "2026-07-02",
        "remarks": "High marks"
    }
    response = client.post("/admissions/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["student_id"] == student["student_id"]
    assert data["course_id"] == course["course_id"]
    assert "admission_id" in data
    assert data["status"] == "Pending Verification"

def test_cancel_admission(client):
    # Setup
    student = client.post("/students/", json={"name": "Rahul", "phone_number": "+919876543210"}).json()
    dept = client.post("/departments/", json={"department_name": "CS Department"}).json()
    course = client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept["department_id"],
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    }).json()
    
    admission = client.post("/admissions/", json={
        "student_id": student["student_id"],
        "course_id": course["course_id"],
        "application_date": "2026-07-02"
    }).json()

    adm_id = admission["admission_id"]
    
    # Cancel test (DELETE endpoint)
    response = client.delete(f"/admissions/{adm_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "Cancelled"

    # Verify status is Cancelled via GET
    get_response = client.get(f"/admissions/{adm_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["status"] == "Cancelled"
