from dataclasses import dataclass


@dataclass
class AuthorRecord:
    id: int
    name: str


@dataclass
class BookRecord:
    id: int
    title: str
    author_id: int


authors = [
    AuthorRecord(id=1, name="Dante Alighieri"),
    AuthorRecord(id=2, name="Cormac McCarthy"),
]

books = [
    BookRecord(id=1, title="The Devine Comedy", author_id=1),
    BookRecord(id=2, title="Blood Meridian", author_id=2),
]