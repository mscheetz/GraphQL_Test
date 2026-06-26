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
                success
                message
                author {
                    id
                    name
                }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addAuthor"]["success"] == False
    assert data["addAuthor"]["message"] == "Author with name Cormac McCarthy exists"
    assert data["addAuthor"]["author"] == None

def test_add_author_mutation_success() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addAuthor(name: "Mario Puzo") {
                success
                message
                author {
                    id
                    name
                }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addAuthor"]["success"] == True
    assert data["addAuthor"]["author"]["name"] == "Mario Puzo"
    assert data["addAuthor"]["author"]["id"] == 3

def test_add_book_mutation_failure() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addBook(title: "The Godfather", authorId: 100) {
                success
                message
                book {
                    id
                    title
                    author {
                        name
                    }
                }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addBook"]["success"] == False
    assert data["addBook"]["message"] == "Author with id 100 does not exist"
    assert data["addBook"]["book"] == None

def test_add_book_mutation_success() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addBook(title: "The Godfather", authorId: 3) {
                success
                message
                book {
                    id
                    title
                    author {
                        name
                    }
                }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addBook"]["success"] == True
    assert data["addBook"]["book"]["author"]["name"] == "Mario Puzo"
    assert data["addBook"]["book"]["title"] == "The Godfather"

def test_add_book_mutation_double_add_failure() -> None:
    response = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
              addBook(title: "The Godfather", authorId: 3) {
                success
                message
                book {
                    id
                    title
                    author {
                        name
                    }
                }
              }
            }
            """
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["addBook"]["success"] == False
    assert data["addBook"]["book"] == None
