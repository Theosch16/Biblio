import pytest
from sqlalchemy.orm import Session

from src.models.users import User
from src.models.books import Book
from src.repositories.loans import LoanRepository
from src.services.loans import LoanService
from src.repositories.users import UserRepository
from src.repositories.books import BookRepository
from src.services.users import UserService
from src.services.books import BookService
from src.api.schemas.users import UserCreate
from src.api.schemas.books import BookCreate
from src.api.schemas.loans import LoanCreate


def create_test_user(db: Session):
    user_repo = UserRepository(User, db)
    user_service = UserService(user_repo)
    return user_service.create(UserCreate(
        email="borrower@example.com",
        password="testpass",
        full_name="Borrower"
    ))


def create_test_book(db: Session):
    book_repo = BookRepository(Book, db)
    book_service = BookService(book_repo)
    return book_service.create(BookCreate(
        title="Borrowable Book",
        author="Author",
        description="Desc",
        available_copies=2
    ))


def test_borrow_book(db_session: Session):
    user = create_test_user(db_session)
    book = create_test_book(db_session)

    loan_repo = LoanRepository(db_session)
    loan_service = LoanService(loan_repo)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    loan = loan_service.borrow_book(loan_in)

    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.returned_at is None


def test_return_book(db_session: Session):
    user = create_test_user(db_session)
    book = create_test_book(db_session)

    loan_repo = LoanRepository(db_session)
    loan_service = LoanService(loan_repo)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    loan = loan_service.borrow_book(loan_in)

    loan_borrow = loan_service.return_book(loan.id)

    assert loan_borrow.returned_at is not None


def test_cannot_borrow_unavailable_book(db_session: Session):
    user1 = create_test_user(db_session)
    user2 = create_test_user(db_session)
    book_repo = BookRepository(Book, db_session)
    book_service = BookService(book_repo)

    book = book_service.create(BookCreate(
        title="Only One Copy",
        author="Author",
        description="",
        available_copies=1
    ))

    loan_repo = LoanRepository(db_session)
    loan_service = LoanService(loan_repo)

    loan_service.borrow_book(LoanCreate(user_id=user1.id, book_id=book.id))

    with pytest.raises(ValueError):
        loan_service.borrow_book(LoanCreate(user_id=user2.id, book_id=book.id))
