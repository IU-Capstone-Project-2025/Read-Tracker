import uuid
from typing import Tuple, List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import date
from src.database.models import Users, Book, Review, Note, Streak, Base, Collection, CollectionItem, UserBook, Subscription, \
    BookTag, Tag

import bcrypt


class DBHandler:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.fixed_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")

    def getReview(self, user_id: Optional[uuid.UUID] = None, book_id: Optional[uuid.UUID] = None) -> Tuple[List[Review], Optional[Exception]]:

        session = self.Session()
        try:
            if not user_id and not book_id:
                return [], ValueError("At least one of user_id or book_id must be provided")
            query = session.query(Review)
            if user_id and book_id:
                query = query.filter_by(user_id=user_id, book_id=book_id)
            elif user_id:
                query = query.filter_by(user_id=user_id)
            elif book_id:
                query = query.filter_by(book_id=book_id)
            reviews = query.all()
            return reviews, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def addReview(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, rate: int = None,
                  text: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if rate is not None and not (0 <= rate <= 10):
                return ValueError("Rate must be between 0 and 10")
            existing = session.query(Review).filter_by(user_id=user_id, book_id=book_id).first()
            if existing:
                return ValueError("Review already exists for this user and book")
            review = Review(user_id=user_id, book_id=book_id, rate=rate, text=text)
            session.add(review)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def updateReview(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, rate: int = None,
                     text: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if rate is not None and not (0 <= rate <= 10):
                return ValueError("Rate must be between 0 and 10")
            review = session.query(Review).filter_by(user_id=user_id, book_id=book_id).first()
            if not review:
                return ValueError("Review not found")
            if rate is not None:
                review.rate = rate
            if text is not None:
                review.text = text
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def deleteReview(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            review = session.query(Review).filter_by(user_id=user_id, book_id=book_id).first()
            if not review:
                return ValueError("Review not found")
            session.delete(review)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getNotes(self, user_id: Optional[uuid.UUID] = None, book_id: Optional[uuid.UUID] = None) -> Tuple[
        List[Note], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if not user_id and not book_id:
                return [], ValueError("At least one of user_id or book_id must be provided")
            query = session.query(Note)
            if user_id and book_id:
                query = query.filter_by(user_id=user_id, book_id=book_id)
            elif user_id:
                query = query.filter_by(user_id=user_id)
            elif book_id:
                query = query.filter_by(book_id=book_id)
            notes = query.all()
            return notes, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def getNote(self, note_id: uuid.UUID) -> Tuple[Optional[Note], Optional[Exception]]:
        session = self.Session()
        try:
            note = session.query(Note).get(note_id)
            if not note:
                return None, ValueError("Note not found")
            return note, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def addNote(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, text: str = None) -> Optional[
        Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            note = Note(user_id=user_id, book_id=book_id, text=text)
            session.add(note)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def updateNote(self, note_id: uuid.UUID, text: str = None) -> Optional[Exception]:
        session = self.Session()
        try:
            note = session.query(Note).get(note_id)
            if not note:
                return ValueError("Note not found")
            if text is not None:
                note.text = text
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def deleteNote(self, note_id: uuid.UUID) -> Optional[Exception]:
        session = self.Session()
        try:
            note = session.query(Note).get(note_id)
            if not note:
                return ValueError("Note not found")
            session.delete(note)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def startStreak(self, user_id: Optional[uuid.UUID] = None, check_date: date = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if not session.query(Users).get(user_id):
                return ValueError(f"User {user_id} not found")
            open_streak = session.query(Streak).filter_by(user_id=user_id, end_date=None).first()
            if open_streak:
                open_streak.last_marked = date.today()
            else:
                new_streak = Streak(
                    user_id=user_id,
                    start_date=check_date or date.today(),
                    last_marked=check_date or date.today(),
                    end_date=None
                )
                session.add(new_streak)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            print(f"Database integrity error starting streak for user {user_id}: {str(e)}")
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error starting streak for user {user_id}: {str(e)}")
            return e
        finally:
            session.close()

    def endStreak(self, user_id: Optional[uuid.UUID] = None, close_date: date = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            streak = session.query(Streak).filter_by(user_id=user_id, end_date=None).first()
            if not streak:
                return ValueError("No open streak found")
            streak.end_date = close_date or date.today()
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getStreaks(self, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Streak], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            streaks = session.query(Streak).filter_by(user_id=user_id).all()
            return streaks, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def getBooks(self) -> Tuple[List[Book], Optional[Exception]]:
        session = self.Session()
        try:
            books = session.query(Book).all()
            return books, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def registerUser(self, name: str, email: str, password: str) -> Optional[Exception]:
        session = self.Session()
        try:
            if session.query(Users).filter_by(mail=email).first():
                return ValueError("Email already exists")
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode()
            user = Users(name=name, mail=email, password=hashed_password_str)
            session.add(user)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def loginUser(self, mail: str, password: str) -> Tuple[Optional[uuid.UUID], Optional[Exception]]:
        session = self.Session()
        try:
            user = session.query(Users).filter_by(mail=mail).first()
            if not user:
                return None, ValueError("No user found with this email")
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                return None, ValueError("Password mismatch")
            return user.id, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def resetPassword(self, user_id: Optional[uuid.UUID] = None, password: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            user = session.query(Users).get(user_id)
            if not user:
                return ValueError("User not found")
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode()
            user.password = hashed_password_str
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getUser(self, user_id: Optional[uuid.UUID] = None) -> Tuple[Optional[Users], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            user = session.query(Users).get(user_id)
            if not user:
                return None, ValueError("User not found")
            return user, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def updateAvatar(self, user_id: Optional[uuid.UUID] = None, avatar: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            user = session.query(Users).get(user_id)
            if not user:
                return ValueError("User not found")
            user.avatar = avatar
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getCollections(self, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Collection], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            collections = session.query(Collection).filter_by(user_id=user_id).all()
            return collections, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def getCollection(self, collection_id: uuid.UUID) -> Tuple[Optional[Collection], Optional[Exception]]:
        session = self.Session()
        try:
            collection = session.query(Collection).get(collection_id)
            if not collection:
                return None, ValueError("Collection not found")
            return collection, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def addCollection(self, user_id: Optional[uuid.UUID] = None, title: str = None, description: str = None,
                      cover: str = None, is_private: bool = False) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if not session.query(Users).get(user_id):
                return ValueError("User not found")
            collection = Collection(user_id=user_id, title=title, description=description, cover=cover,
                                    is_private=is_private)
            session.add(collection)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def updateCollection(self, collection_id: uuid.UUID, title: str = None, description: str = None,
                         cover: str = None, is_private: bool = None) -> Optional[Exception]:
        session = self.Session()
        try:
            collection = session.query(Collection).get(collection_id)
            if not collection:
                return ValueError("Collection not found")
            if title is not None:
                collection.title = title
            if description is not None:
                collection.description = description
            if cover is not None:
                collection.cover = cover
            if is_private is not None:
                collection.is_private = is_private
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def deleteCollection(self, collection_id: uuid.UUID) -> Optional[Exception]:
        session = self.Session()
        try:
            collection = session.query(Collection).get(collection_id)
            if not collection:
                return ValueError("Collection not found")
            session.delete(collection)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def addBookToCollection(self, collection_id: uuid.UUID, book_id: uuid.UUID) -> Optional[Exception]:
        session = self.Session()
        try:
            # Verify collection and book exist
            if not session.query(Collection).get(collection_id):
                return ValueError("Collection not found")
            if not session.query(Book).get(book_id):
                return ValueError("Book not found")
            # Check if book is already in collection
            if session.query(CollectionItem).filter_by(collection_id=collection_id, book_id=book_id).first():
                return ValueError("Book already in collection")
            collection_item = CollectionItem(collection_id=collection_id, book_id=book_id)
            session.add(collection_item)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def deleteBookFromCollection(self, collection_id: uuid.UUID, book_id: uuid.UUID) -> Optional[Exception]:
        session = self.Session()
        try:
            collection_item = session.query(CollectionItem).filter_by(collection_id=collection_id,
                                                                      book_id=book_id).first()
            if not collection_item:
                return ValueError("Book not found in collection")
            session.delete(collection_item)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getBook(self, book_id: uuid.UUID) -> Tuple[Optional[Book], Optional[Exception]]:
        session = self.Session()
        try:
            book = session.query(Book).get(book_id)
            if not book:
                return None, ValueError("Book not found")
            return book, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def getUserBooks(self, user_id: Optional[uuid.UUID] = None) -> Tuple[List[Book], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            user_books = session.query(UserBook).filter_by(user_id=user_id).all()
            books = []
            for ub in user_books:
                book = ub.book
                if book:
                    books.append(book)
                else:
                    print(f"Book with ID {ub.book_id} not found for user {user_id}")
            return user_books, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def getUserBook(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None) -> Tuple[
        Optional[Book], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        if book_id is None:
            return None, ValueError("book_id must be provided")
        session = self.Session()
        try:
            user_book = session.query(UserBook).filter_by(user_id=user_id, book_id=book_id).first()
            if not user_book:
                return None, ValueError(f"No association found for user {user_id} and book {book_id}")
            book = user_book.book
            if not book:
                return None, ValueError(f"Book {book_id} not found")
            return user_book, None
        except SQLAlchemyError as e:
            return None, e
        finally:
            session.close()

    def updateUserBook(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, status: str = None) -> \
            Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        if book_id is None or status is None:
            return ValueError("book_id and status must be provided")
        session = self.Session()
        try:
            user_book = session.query(UserBook).filter_by(user_id=user_id, book_id=book_id).first()
            if not user_book:
                return ValueError(f"No association found for user {user_id} and book {book_id}")
            if status not in ['want to read', 'reading now', 'have read']:
                return ValueError(f"Invalid status: {status}")
            user_book.status = status
            if status == 'reading now':
                user_book.start_date = date.today()
                user_book.end_date = None
            elif status == 'have read':
                user_book.end_date = date.today()
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def deleteUserBook(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        if book_id is None:
            return ValueError("book_id must be provided")
        session = self.Session()
        try:
            user_book = session.query(UserBook).filter_by(user_id=user_id, book_id=book_id).first()
            if not user_book:
                return ValueError(f"No association found for user {user_id} and book {book_id}")
            session.delete(user_book)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            return e
        finally:
            session.close()

    def getCollectionItems(self, collection_id: uuid.UUID = None) -> Tuple[List[Book], Optional[Exception]]:
        if collection_id is None:
            return [], ValueError("collection_id must be provided")
        session = self.Session()
        try:
            collection_items = session.query(CollectionItem).filter_by(collection_id=collection_id).all()
            books = []
            print(f"Collection items: {collection_items}")
            for ci in collection_items:
                book = ci.book
                if book:
                    books.append(book)
                else:
                    print(f"Book with ID {ci.book_id} not found in collection {collection_id}")
            return books, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def addUserBook(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, status: str = None) -> \
            Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        if book_id is None or status is None:
            return ValueError("book_id and status must be provided")
        session = self.Session()
        try:
            if not session.query(Users).get(user_id):
                return ValueError(f"User {user_id} not found")
            if not session.query(Book).get(book_id):
                return ValueError(f"Book {book_id} not found")
            if session.query(UserBook).filter_by(user_id=user_id, book_id=book_id).first():
                return ValueError(f"User {user_id} already has book {book_id}")
            if status not in ['want to read', 'reading now', 'have read']:
                return ValueError(f"Invalid status: {status}")
            user_book = UserBook(
                user_id=user_id,
                book_id=book_id,
                status=status,
                start_date=date.today() if status == 'reading now' else None,
                end_date=date.today() if status == 'have read' else None
            )
            session.add(user_book)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            print(f"Database integrity error adding user book {book_id} for user {user_id}: {str(e)}")
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error adding user book {book_id} for user {user_id}: {str(e)}")
            return e
        finally:
            session.close()

    def addSubscription(self, follower_id: Optional[uuid.UUID] = None, subscribed_id: uuid.UUID = None) -> Optional[
        Exception]:
        if follower_id is None:
            follower_id = self.fixed_user_id
        if subscribed_id is None:
            return ValueError("subscribed_id must be provided")
        session = self.Session()
        try:
            if not session.query(Users).get(follower_id):
                return ValueError(f"Follower user {follower_id} not found")
            if not session.query(Users).get(subscribed_id):
                return ValueError(f"Subscribed user {subscribed_id} not found")
            if session.query(Subscription).filter_by(follower_id=follower_id, subscribed_id=subscribed_id).first():
                return ValueError(
                    f"Subscription already exists for follower {follower_id} and subscribed {subscribed_id}")
            if follower_id == subscribed_id:
                return ValueError("Users cannot subscribe to themselves")
            subscription = Subscription(follower_id=follower_id, subscribed_id=subscribed_id)
            session.add(subscription)
            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            print(
                f"Database integrity error adding subscription for follower {follower_id} to subscribed {subscribed_id}: {str(e)}")
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            print(
                f"Error adding subscription for follower {follower_id} to subscribed {subscribed_id}: {str(e)}")
            return e
        finally:
            session.close()

    def deleteSubscription(self, follower_id: Optional[uuid.UUID] = None, subscribed_id: uuid.UUID = None) -> Optional[
        Exception]:
        if follower_id is None:
            follower_id = self.fixed_user_id
        if subscribed_id is None:
            return ValueError("subscribed_id must be provided")
        session = self.Session()
        try:
            subscription = session.query(Subscription).filter_by(follower_id=follower_id,
                                                                 subscribed_id=subscribed_id).first()
            if not subscription:
                return ValueError(f"No subscription found for follower {follower_id} and subscribed {subscribed_id}")
            session.delete(subscription)
            session.commit()
            return None
        except SQLAlchemyError as e:
            session.rollback()
            print(
                f"Error deleting subscription for follower {follower_id} and subscribed {subscribed_id}: {str(e)}")
            return e
        finally:
            session.close()

    def getAllReviews(self, follower_id: Optional[uuid.UUID] = None) -> Tuple[List[Review], Optional[Exception]]:
        if follower_id is None:
            follower_id = self.fixed_user_id
        session = self.Session()
        try:
            if not session.query(Users).get(follower_id):
                return [], ValueError(f"Follower user {follower_id} not found")
            subscriptions = session.query(Subscription).filter_by(follower_id=follower_id).all()
            subscribed_ids = [sub.subscribed_id for sub in subscriptions]
            if not subscribed_ids:
                return [], None
            reviews = session.query(Review).filter(Review.user_id.in_(subscribed_ids)).all()
            return reviews, None
        except SQLAlchemyError as e:
            print(f"Error retrieving reviews for follower {follower_id}: {str(e)}")
            return [], e
        finally:
            session.close()

    def setTags(self, book_title: str, tags: List[str]) -> Optional[Exception]:
        if not book_title or not tags:
            return ValueError("book_name and tags must be provided and non-empty")
        session = self.Session()
        try:
            book = session.query(Book).filter_by(title=book_title).first()
            if not book:
                print(f"Book with name '{book_title}' not found")
                return ValueError(f"Book with name '{book_title}' not found")
            book_id = book.id

            for tag_name in tags:
                if not tag_name:
                    continue
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if not tag:
                    print(f"Tag with name '{tag_name}' not found")
                    return ValueError(f"Tag with name '{tag_name}' not found")
                existing_book_tag = session.query(BookTag).filter_by(book_id=book_id, tag_id=tag.id).first()
                if not existing_book_tag:
                    book_tag = BookTag(book_id=book_id, tag_id=tag.id)
                    session.add(book_tag)

            session.commit()
            return None
        except IntegrityError as e:
            session.rollback()
            print(f"Database integrity error setting tags for book '{book_title}': {str(e)}")
            return ValueError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error setting tags for book '{book_title}': {str(e)}")
            return e
        finally:
            session.close()

    def getPublisherReviews(self, follower_id: Optional[uuid.UUID] = None, publisher_id: uuid.UUID = None) -> \
            Tuple[List[Review], Optional[Exception]]:
        if follower_id is None:
            follower_id = self.fixed_user_id
        session = self.Session()
        try:
            if not session.query(Users).get(follower_id):
                return [], ValueError(f"Follower user {follower_id} not found")
            if not session.query(Users).get(publisher_id):
                return [], ValueError(f"Publisher user {publisher_id} not found")
            subscription = session.query(Subscription).filter_by(follower_id=follower_id,
                                                                 subscribed_id=publisher_id).first()
            if not subscription:
                return [], ValueError(f"User {follower_id} is not subscribed on publisher {publisher_id}")
            return self.getReview(user_id=publisher_id)

        except SQLAlchemyError as e:
            print(f"Error retrieving reviews for follower {follower_id}: {str(e)}")
            return [], e
        finally:
            session.close()

    def getBookReviews(self, book_id: Optional[uuid.UUID] = None) -> Tuple[List[Review], Optional[Exception]]:
        if book_id is None:
            return [], ValueError(f"book_id was not provided")
        session = self.Session()
        try:
            if not session.query(Book).get(book_id):
                return [], ValueError(f"Book {book_id} not found")
            return self.getReview(book_id=book_id)
        except SQLAlchemyError as e:
            print(f"Error retrieving reviews for book {book_id}: {str(e)}")
            return [], e
        finally:
            session.close()

    def getTags(self, book_id: uuid.UUID) -> Tuple[List[Tag], Optional[Exception]]:
        if book_id is None:
            return [], ValueError("book_id must be provided")
        session = self.Session()
        try:
            if not session.query(Book).get(book_id):
                return [], ValueError(f"Book with ID {book_id} not found")
            book_tags = session.query(BookTag).filter_by(book_id=book_id).all()
            if not book_tags:
                return [], None
            tag_ids = [bt.tag_id for bt in book_tags]
            tags = session.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            return tags, None
        except SQLAlchemyError as e:
            print(f"Error retrieving tags for book {book_id}: {str(e)}")
            return [], e
        finally:
            session.close()

    def getPublishers(self, follower_id: Optional[uuid.UUID] = None) -> Tuple[List[Users], Optional[Exception]]:
        session = self.Session()
        try:
            if not session.query(Users).get(follower_id):
                return [], ValueError(f"Follower user {follower_id} not found")
            subscriptions = session.query(Subscription).filter_by(follower_id=follower_id).all()
            subscribed_ids = [sub.subscribed_id for sub in subscriptions]
            if not subscribed_ids:
                return [], None
            publishers = session.query(Users).filter(Users.id.in_(subscribed_ids)).all()
            return publishers, None
        except SQLAlchemyError as e:
            print(f"Error retrieving reviews for follower {follower_id}: {str(e)}")
            return [], e
        finally:
            session.close()
