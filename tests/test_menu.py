from fastapi import status

def test_create_menu_item(client):
    payload = {
        "name": "Spaghetti Carbonara",
        "description": "Pasta with pancetta and creamy sauce",
        "price": 18.50,
        "category": "entrees",
        "is_available": True
    }
    response = client.post("/menu/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Spaghetti Carbonara"
    assert float(data["price"]) == 18.50

def test_search_menu_items(client):
    # Setup multiple menu items
    client.post("/menu/", json={
        "name": "Margherita Pizza",
        "description": "Tomato mozzarella and basil",
        "price": 14.00,
        "category": "entrees"
    })
    client.post("/menu/", json={
        "name": "Garlic Bread",
        "description": "Baked bread with garlic butter",
        "price": 6.50,
        "category": "appetizers"
    })

    # Search for pizza
    response = client.get("/menu/search?q=pizza")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Margherita Pizza"

    # Search for garlic
    response2 = client.get("/menu/search?q=garlic")
    assert response2.status_code == status.HTTP_200_OK
    data2 = response2.json()
    assert len(data2) == 1
    assert data2[0]["name"] == "Garlic Bread"
