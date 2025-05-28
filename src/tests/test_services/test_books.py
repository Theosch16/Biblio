import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate


def test_create_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="1984",
        author="George Orwell",
        description="Dystopie",
        available_copies=3
    )

    book = service.create(obj_in=book_in)

    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.description == "Dystopie"
    assert book.available_copies == 3


def test_update_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="To Update",
    )