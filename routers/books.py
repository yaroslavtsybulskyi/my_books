import time

from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from models import Book, Author, Publisher
from schemas import BookBase, BookUpdate, AuthorCreate, PublisherCreate, BookOut, AuthorOut, PublisherOut
from database import get_db

router = APIRouter()


def notify_about_new_book(title: str) -> None:
    """
    Simulates a background task for notifying when a new book is added.
    :param title: The title of the newly added book.
    """
    time.sleep(2)
    print(f"Background Task: New book was added: {title}")


@router.post("/books/", response_model=BookOut)
def create_book(book: BookBase, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Create a new book with optional authors and a publisher.
    A background task will be triggered after creation.
    :param book: Book input data.
    :param background_tasks: FastAPI background task handler.
    :param db: SQLAlchemy DB session.
    :return: Created book object.
    """
    db_book = Book(title=book.title, publisher_id=book.publisher_id)
    db_book.authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    background_tasks.add_task(notify_about_new_book, title=book.title)
    return db_book


@router.get("/books/{id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    """
    Retrieve a book by ID.
    :param book_id: The ID of the book.
    :param db: DB session.
    :return: Book object or raises 404.
    """
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get('/books/', response_model=List[BookOut])
def get_all_books(db: Session = Depends(get_db)):
    """
    Get a list of all books in the library.
    :param db: DB session.
    :return: List of all books in the library.
    """
    return db.query(Book).all()


@router.patch("/books/{id}", response_model=BookOut)
def update_book(book_id: int, update: BookUpdate, db: Session = Depends(get_db)) -> Book:
    """
    Partially update a book by ID.
    :param book_id: ID of the book to update.
    :param update: Fields to update.
    :param db: DB session.
    :return: Updated book object.
    """
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if update.title:
        book.title = update.title
    if update.publisher_id:
        book.publisher_id = update.publisher_id
    if update.author_ids is not None:
        book.authors = db.query(Author).filter(Author.id.in_(update.author_ids)).all()
    db.commit()
    return book


@router.delete("/books/{id}")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a book by ID.
    :param book_id: ID of the book to delete.
    :param db: DB session.
    :return: Confirmation message.
    """
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}


@router.get("/authors/", response_model=List[AuthorOut])
def get_all_authors(db: Session = Depends(get_db)):
    """
    Get a list of all authors.
    :param db: DB session.
    :return: List of authors.
    """
    return db.query(Author).all()


@router.post("/authors/", response_model=AuthorOut)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)) -> Author:
    """
    Create a new author.
    :param author: Author input data.
    :param db: DB session.
    :return: Created author object.
    """
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/publishers/", response_model=List[PublisherOut])
def get_all_publishers(db: Session = Depends(get_db)):
    """
    Get a list of all publishers.
    :param db: DB session.
    :return: List of publishers.
    """
    return db.query(Publisher).all()


@router.post("/publishers/", response_model=PublisherOut)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db)):
    """
    Create a new publisher.
    :param publisher: Publisher input data.
    :param db: DB session.
    :return: Created publisher object.
    """
    db_publisher = Publisher(name=publisher.name)
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher
