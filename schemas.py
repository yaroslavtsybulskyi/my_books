from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    """
    Shared properties for creating/updating a book.
    """

    title: str
    publisher_id: Optional[int]
    author_ids: List[int] = []


class BookUpdate(BaseModel):
    """
    Schema for partial update of a book.
    All fields are optional.
    """

    title: Optional[str] = None
    publisher_id: Optional[int] = None
    author_ids: Optional[List[int]] = None


class AuthorCreate(BaseModel):
    """
    Schema for creating an author.
    """

    name: str


class PublisherCreate(BaseModel):
    """
    Schema for creating publisher.
    """

    name: str


class AuthorOut(BaseModel):
    """
    Schema for returning author data.
    """

    id: int
    name: str

    class Config:
        from_attributes = True


class BookOut(BaseModel):
    """
    Schema for returning book data with nested author info.
    """

    id: int
    title: str
    publisher_id: Optional[int]
    authors: List[AuthorOut] = []

    class Config:
        from_attributes = True


class PublisherOut(BaseModel):
    """
    Schema for returning publisher data.
    """

    id: int
    name: str

    class Config:
        from_attributes = True
