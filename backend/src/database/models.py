import uuid
from sqlalchemy import (
    Column, Integer, Text, Boolean, ForeignKey, Date, DateTime, CheckConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    mail = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    avatar = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    collections = relationship("Collection", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    notes = relationship("Note", back_populates="user")
    streaks = relationship("Streak", back_populates="user")
    user_books = relationship("UserBook", back_populates="user")
    followers = relationship("Subscription", back_populates="followed", foreign_keys="Subscription.subscribed_id")
    following = relationship("Subscription", back_populates="follower", foreign_keys="Subscription.follower_id")


class Book(Base):
    __tablename__ = "book"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    __tablename__ = "tag"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text)

    books = relationship("BookTag", back_populates="tag")


class BookTag(Base):
    __tablename__ = "book_tag"

    tag_id = Column(UUID, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(UUID, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)

    tag = relationship("Tag", back_populates="books")
    book = relationship("Book", back_populates="tags")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)
    cover = Column(Text)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("Users", back_populates="collections")
    items = relationship("CollectionItem", back_populates="collection", cascade="all, delete-orphan")


class CollectionItem(Base):
    __tablename__ = "collection_item"

    collection_id = Column(UUID, ForeignKey("collection.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(UUID, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    content_type = Column(Text)

    collection = relationship("Collection", back_populates="items")
    book = relationship("Book", back_populates="collections")


class Review(Base):
    __tablename__ = "review"

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(UUID, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    rate = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("rate BETWEEN 0 AND 10", name="check_review_rate"),
    )

    user = relationship("Users", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class Note(Base):
    __tablename__ = "note"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    book_id = Column(UUID, ForeignKey("book.id", ondelete="CASCADE"))
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("Users", back_populates="notes")
    book = relationship("Book", back_populates="notes")


class UserBook(Base):
    __tablename__ = "user_book"

    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(UUID, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Text)

    __table_args__ = (
        CheckConstraint("status IN ('want to read', 'reading now', 'have read')", name="check_userbook_status"),
    )

    user = relationship("Users", back_populates="user_books")
    book = relationship("Book", back_populates="user_books")


class Streak(Base):
    __tablename__ = "streak"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"))
    start_date = Column(Date)
    end_date = Column(Date)
    last_marked = Column(Date)

    user = relationship("Users", back_populates="streaks")


class Subscription(Base):
    __tablename__ = "subscription"

    follower_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    subscribed_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    follower = relationship("Users", back_populates="following", foreign_keys=[follower_id])
    followed = relationship("Users", back_populates="followers", foreign_keys=[subscribed_id])
