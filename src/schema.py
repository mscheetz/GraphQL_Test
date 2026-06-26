from __future__ import annotations

from typing import Optional

import strawberry

from src.data import AuthorRecord, BookRecord, authors, books


@strawberry.type
class Author:
    id: int
    name: str


@strawberry.type
class Book:
    id: int
    title: str
    author_id: strawberry.Private[int]

    @strawberry.field
    def author(self) -> Optional[Author]:
        record = next((author for author in authors if author.id == self.author_id), None)
        if record is None:
            return None
        return Author(id=record.id, name=record.name)

@strawberry.type
class MutationResult:
    success: bool
    message: str

@strawberry.type
class AddAuthorResult(MutationResult):
    author: Author | None

@strawberry.type
class AddBookResult(MutationResult):
    book: Book | None

def to_book(record: BookRecord) -> Book:
    return Book(id=record.id, title=record.title, author_id=record.author_id)

def to_author(record: AuthorRecord) -> Author:
    return Author(id=record.id, name=record.name)


@strawberry.type
class Query:
    @strawberry.field
    async def hello(self) -> str:
        return "Hello World!"

    @strawberry.field
    async def books(self) -> list[Book]:
        return [to_book(book) for book in books]

    @strawberry.field
    async def book(self, id: int) -> Optional[Book]:
        record = next((book for book in books if book.id == id), None)
        return to_book(record) if record else None

    @strawberry.field
    async def authors(self) -> list[Author]:
        return [to_author(author) for author in authors]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_author(self, name: str) -> AddAuthorResult:
        author_exists = any(author.name == name for author in authors)
        if author_exists:
            return AddAuthorResult(
                success=False,
                message=f"Author with name {name} exists",
                author=None
            )

        next_id = max((author.id for author in authors), default=0) + 1
        record = AuthorRecord(id=next_id, name=name)
        authors.append(record)

        return AddAuthorResult(
            success=True,
            message="Author added.",
            author=to_author(record)
        ) 

    @strawberry.mutation
    async def delete_author(self, id: int) -> MutationResult:
        if any(book.author_id == id for book in books):
            return MutationResult(
                success=False,
                message="Author has books and cannot be deleted."
            )

        for index, author in enumerate(authors):
            if author.id == id:
                del authors[index]
                return MutationResult(
                    success=True,
                    message="Author deleted."
                )

        return MutationResult(
            success=False,
            message="Author not found"
        )

    @strawberry.mutation
    async def add_book(self, title: str, author_id: int) -> AddBookResult:
        author_exists = any(author.id == author_id for author in authors)
        if not author_exists:
            return AddBookResult(
                success=False,
                message=f"Author with id {author_id} does not exist",
                book=None
            )

        if any(book.title == title and book.author_id == author_id for book in books):
            return AddBookResult(
                success=False,
                message=f"Book '{title}' by author {author_id} already exists",
                book=None
            )

        next_id = max((book.id for book in books), default=0) + 1
        record = BookRecord(id=next_id, title=title, author_id=author_id)
        books.append(record)

        return AddBookResult(
            success=True,
            message="Book added",
            book=to_book(record)
        )

    @strawberry.mutation
    async def delete_book(self, id: int) -> MutationResult:
        for index, book in enumerate(books):
            if book.id == id:
                del books[index]
                return MutationResult(
                    success=True,
                    message="Book deleted."
                )

        return MutationResult(
            success=False,
            message="Book not found"
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)