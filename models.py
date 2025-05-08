from typing import List
from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

book_author = Table(
    "book_author", Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True)
)


class Publisher(Base):
    """
    Represents a book publisher.
    One publisher can publish many books.
    """

    __tablename__ = "publishers"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True)
    books = relationship("Book", back_populates="publisher")


class Author(Base):
    """
    Represents an author.
    One author can write many books.
    One book can be written by many authors.
    """

    __tablename__ = "authors"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True)
    books = relationship("Book", secondary=book_author, back_populates="authors")


class Book(Base):
    """
    Represents a book.
    Each book has one publisher and may have multiple authors.
    """

    __tablename__ = "books"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)
    publisher_id: int = Column(Integer, ForeignKey("publishers.id"))
    publisher = relationship("Publisher", back_populates="books")
    authors = relationship("Author", secondary=book_author, back_populates="books")
