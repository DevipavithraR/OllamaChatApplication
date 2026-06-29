from fastapi import status

def test_movie_crud(client):
    # Create movie
    payload = {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "language": "English",
        "duration": "169 min",
        "rating": "PG-13",
        "description": "A journey to another galaxy",
        "release_date": "2014-11-07"
    }
    res = client.post("/movies", json=payload)
    assert res.status_code == status.HTTP_200_OK
    movie = res.json()
    assert movie["title"] == "Interstellar"
    assert "movie_id" in movie

    # Search movie
    search_res = client.get("/movies/search?title=Inter")
    assert search_res.status_code == status.HTTP_200_OK
    assert len(search_res.json()) >= 1

def test_theatre_crud(client):
    payload = {
        "theatre_name": "PVR Cinemas",
        "location": "Mall of India",
        "screens": 4
    }
    res = client.post("/theatres", json=payload)
    assert res.status_code == status.HTTP_200_OK
    theatre = res.json()
    assert theatre["theatre_name"] == "PVR Cinemas"
    assert "theatre_id" in theatre

def test_show_crud(client):
    # Setup Movie and Theatre
    movie = client.post("/movies", json={
        "title": "Inception",
        "genre": "Sci-Fi",
        "language": "English",
        "duration": "148 min",
        "rating": "PG-13"
    }).json()

    theatre = client.post("/theatres", json={
        "theatre_name": "IMAX Forum",
        "location": "Forum Mall",
        "screens": 2
    }).json()

    # Create Show
    payload = {
        "movie_id": movie["movie_id"],
        "theatre_id": theatre["theatre_id"],
        "screen_number": 1,
        "show_datetime": "2026-07-20T14:30:00",
        "ticket_price": 300.0,
        "available_seats": 50,
        "total_seats": 50
    }
    res = client.post("/shows", json=payload)
    assert res.status_code == status.HTTP_200_OK
    show = res.json()
    assert show["movie_id"] == movie["movie_id"]
    assert show["theatre_id"] == theatre["theatre_id"]
