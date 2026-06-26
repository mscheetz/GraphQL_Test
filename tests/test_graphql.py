from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_hello_query() -> None:
    response = client.post("/graphql", json={"query": "query { hello }"})

    assert response.status_code == 200
    assert response.json()["data"]["hello"] == "Hello World!"


def test_books_query() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            query {
              books {
                title
                author { name }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["books"][0]["title"] == "The Devine Comedy"
    assert data["books"][0]["author"]["name"] == "Dante Alighieri"

def test_add_author_mutation_failure() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addAuthor(name: "Cormac McCarthy") {
                id
                name
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data is None
    errors = response.json()["errors"]
    assert errors[0]["message"] == "Author with name Cormac McCarthy exists"

def test_add_author_mutation_success() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addAuthor(name: "Mario Puzo") {
                id
                name
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addAuthor"]["name"] == "Mario Puzo"
    assert data["addAuthor"]["id"] == 3

def test_add_book_mutation_failure() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addBook(title: "The Godfather", authorId: 100) {
                title
                author { name }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data is None
    errors = response.json()["errors"]
    assert errors[0]["message"] == "Author with id 100 does not exist"

def test_add_book_mutation_success() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addBook(title: "The Godfather", authorId: 3) {
                title
                author { name }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]    
    assert data["addBook"]["author"]["name"] == "Mario Puzo"
    assert data["addBook"]["title"] == "The Godfather"
