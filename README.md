# Python GraphQL Sample Project

A small local GraphQL API using **FastAPI** and **Strawberry GraphQL**.

## Features

- Query books and authors
- Create a book with a GraphQL mutation
- Interactive GraphQL UI at `/graphql`
- Basic tests with pytest

## Quick start

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/graphql
```

## Queries

Get books:
```graphql
query {
  books {
    id
    title
    author {
      name
    }
  }
}
```

Get authors:
```graphql
query {
    authors {
        id
        name
    }
}
```

## Mutations

Add Author
```graphql
mutation {
  addAuthor(name: "Mario Puzo") {
    id
    name
  }
}
```

Add Book
```graphql
mutation {
  addBook(title: "The Godfather", authorId: 3) {
    id
    title
    author {
      name
    }
  }
}
```

Delete Author
```graphql
mutation {
    deleteAuthor(id: 3) {
        success
        message
    }
}
```

Delete Book
```graphql
mutation {
    deleteBook(id: 3) {
        success
        message
    }
}
```