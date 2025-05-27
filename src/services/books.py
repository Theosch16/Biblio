from typing import Optional, List, Any, Dict, Union
from sqlalchemy.orm import Session

from ..repositories.books import BookRepository
from ..models.users import User
from ..api.schemas.books import BookCreate, BookUpdate, Book
from ..utils.security import get_password_hash, verify_password
from .base import BaseService


class BookService(BaseService[Book, BookCreate, BookUpdate]):
    """
    Service pour la gestion des livres.
    """
    def get_by_isbn(self, db: Session, *, isbn: str) -> Book:
        """
        Récupère un livre par son ISBN.
        """
        return db.query(Book).filter(Book.isbn == isbn).first()

    def get_by_title(self, db: Session, *, title: str) -> List[Book]:
        """
        Récupère des livres par leur titre (recherche partielle).
        """
        return db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    def get_by_author(self, db: Session, *, author: str) -> List[Book]:
        """
        Récupère des livres par leur auteur (recherche partielle).
        """
        return db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()
    
    
    
    def create(self, *, obj_in: BookCreate) -> Book:
        """
        Crée un nouveau livre.
        """
        # Vérifier si le livre existe déjà
        existing_book = self.get_by_isbn(isbn=obj_in.isbn)
        if existing_book:
            raise ValueError("Le livre existe déjà")


        return self.repository.create(obj_in=obj_in)


    def update_quantity(self, *, book_id: int, quantity_change: int) -> Book:
        """
        Met à jour la quantité d'un livre.
        """
        book = self.get(id=book_id)
        if not book:
            raise ValueError(f"Livre avec l'ID {book_id} non trouvé")

        new_quantity = book.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("La quantité ne peut pas être négative")

        return self.repository.update(db_obj=book, obj_in={"quantity": new_quantity})
       

   