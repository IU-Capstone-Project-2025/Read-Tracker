import uuid
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey, Date, DateTime, CheckConstraint,
    UniqueConstraint, Table, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    mail = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    avatar = Column(Text)

    collections = relationship("Collection", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    notes = relationship("Note", back_populates="user")
    streaks = relationship("Streak", back_populates="user")
    user_books = relationship("UserBook", back_populates="user")
    # the sub
    followers = relationship("Subscription", back_populates="followed", foreign_keys="Subscription.subscribed_id")
    # the author
    following = relationship("Subscription", back_populates="follower", foreign_keys="Subscription.follower_id")


class Book(Base):
    __tablename__ = "Book"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author = Column(Text)
    title = Column(Text, nullable=False)
    language = Column(Text)
    description = Column(Text)
    cover = Column(Text)

    tags = relationship("BookTag", back_populates="book")
    collections = relationship("CollectionItem", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    notes = relationship("Note", back_populates="book")
    user_books = relationship("UserBook", back_populates="book")


class Tag(Base):
    __tablename__ = "Tag"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)

    books = relationship("BookTag", back_populates="tag")


class BookTag(Base):
    __tablename__ = "BookTag"

    tag_ID = Column(UUID, ForeignKey("Tag.ID", ondelete="CASCADE"), primary_key=True)
    book_ID = Column(UUID, ForeignKey("Book.ID", ondelete="CASCADE"), primary_key=True)

    tag = relationship("Tag", back_populates="books")
    book = relationship("Book", back_populates="tags")


class Collection(Base):
    __tablename__ = "Collection"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    user_ID = Column(UUID, ForeignKey("User.ID", ondelete="SET NULL"))
    description = Column(Text)
    cover = Column(Text)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="collections")
    items = relationship("CollectionItem", back_populates="collection")


class CollectionItem(Base):
    __tablename__ = "CollectionItem"

    collection_ID = Column(UUID, ForeignKey("Collection.ID", ondelete="CASCADE"), primary_key=True)
    book_ID = Column(UUID, ForeignKey("Book.ID", ondelete="CASCADE"), primary_key=True)
    content_type = Column(Text)

    collection = relationship("Collection", back_populates="items")
    book = relationship("Book", back_populates="collections")


class Review(Base):
    __tablename__ = "Review"

    user_ID = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"), primary_key=True)
    book_ID = Column(UUID, ForeignKey("Book.ID", ondelete="CASCADE"), primary_key=True)
    rate = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("rate BETWEEN 0 AND 10", name="check_review_rate"),
    )

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class Note(Base):
    __tablename__ = "Note"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_ID = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"))
    book_ID = Column(UUID, ForeignKey("Book.ID", ondelete="CASCADE"))
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="notes")
    book = relationship("Book", back_populates="notes")


class UserBook(Base):
    __tablename__ = "UserBook"

    user_ID = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"), primary_key=True)
    book_ID = Column(UUID, ForeignKey("Book.ID", ondelete="CASCADE"), primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Text)

    __table_args__ = (
        CheckConstraint("status IN ('want to read', 'reading now', 'have read')", name="check_userbook_status"),
    )

    user = relationship("User", back_populates="user_books")
    book = relationship("Book", back_populates="user_books")


class Streak(Base):
    __tablename__ = "Streak"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_ID = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"))
    start_date = Column(Date)
    end_date = Column(Date)

    user = relationship("User", back_populates="streaks")


class Subscription(Base):
    __tablename__ = "Subscription"

    follower_id = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"), primary_key=True)
    subscribed_id = Column(UUID, ForeignKey("User.ID", ondelete="CASCADE"), primary_key=True)

    # the author
    follower = relationship("User", back_populates="following", foreign_keys=[follower_id])
    # the sub
    followed = relationship("User", back_populates="followers", foreign_keys=[subscribed_id])

note = Note()
note.ID