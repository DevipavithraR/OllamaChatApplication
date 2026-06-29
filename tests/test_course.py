from fastapi import status

def test_create_course(client):
    # Setup department first
    dept = client.post("/departments/", json={
        "department_name": "Computer Science Department",
        "description": "AI, Software",
        "head_of_department": "Dr. Turing"
    }).json()
    dept_id = dept["department_id"]

    payload = {
        "course_name": "B.Tech Computer Science",
        "department_id": dept_id,
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%",
        "description": "Core computing course"
    }
    response = client.post("/courses/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["course_name"] == "B.Tech Computer Science"
    assert data["fees"] == 85000.00
    assert "course_id" in data

def test_get_courses(client):
    dept = client.post("/departments/", json={
        "department_name": "Computer Science Department",
        "description": "AI, Software"
    }).json()
    dept_id = dept["department_id"]

    client.post("/courses/", json={
        "course_name": "B.Tech Computer Science",
        "department_id": dept_id,
        "duration": "4 Years",
        "total_seats": 30,
        "available_seats": 25,
        "fees": 85000.00,
        "eligibility": "Minimum 60%"
    })
    
    response = client.get("/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1
