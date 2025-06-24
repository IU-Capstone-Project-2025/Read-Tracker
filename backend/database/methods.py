import uuid
from typing import Tuple, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import date
from models import User, Book, Review, Note, Streak, Base  # Assuming models are in a separate module


class DBHandler:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.fixed_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")  # Fixed UUID for user_id=1

    def getReview(self, user_id: Optional[uuid.UUID] = None, book_id: Optional[uuid.UUID] = None) -> Tuple[List[Review], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if not user_id and not book_id:
                return [], ValueError("At least one of user_id or book_id must be provided")
            query = session.query(Review)
            if user_id and book_id:
                query = query.filter_by(user_ID=user_id, book_ID=book_id)
            elif user_id:
                query = query.filter_by(user_ID=user_id)
            elif book_id:
                query = query.filter_by(book_ID=book_id)
            reviews = query.all()
            return reviews, None
        except SQLAlchemyError as e:
            return [], e
        finally:
            session.close()

    def addReview(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, rate: int = None, text: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if rate is not None and not (0 <= rate <= 10):
                return ValueError("Rate must be between 0 and 10")
            # Check if review exists
            existing = session.query(Review).filter_by(user_ID=user_id, book_ID=book_id).first()
            if existing:
                return ValueError("Review already exists for this user and book")
            review = Review(user_ID=user_id, book_ID=book_id, rate=rate, text=text)
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

    def updateReview(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, rate: int = None, text: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if rate is not None and not (0 <= rate <= 10):
                return ValueError("Rate must be between 0 and 10")
            review = session.query(Review).filter_by(user_ID=user_id, book_ID=book_id).first()
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
            review = session.query(Review).filter_by(user_ID=user_id, book_ID=book_id).first()
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

    def getNotes(self, user_id: Optional[uuid.UUID] = None, book_id: Optional[uuid.UUID] = None) -> Tuple[List[Note], Optional[Exception]]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            if not user_id and not book_id:
                return [], ValueError("At least one of user_id or book_id must be provided")
            query = session.query(Note)
            if user_id and book_id:
                query = query.filter_by(user_ID=user_id, book_ID=book_id)
            elif user_id:
                query = query.filter_by(user_ID=user_id)
            elif book_id:
                query = query.filter_by(book_ID=book_id)
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

    def addNote(self, user_id: Optional[uuid.UUID] = None, book_id: uuid.UUID = None, text: str = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            note = Note(user_ID=user_id, book_ID=book_id, text=text)
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

    # --- Streak Methods ---

    def startStreak(self, user_id: Optional[uuid.UUID] = None, check_date: date = None) -> Optional[Exception]:
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            # Check for open streak (end_date is NULL)
            open_streak = session.query(Streak).filter_by(user_ID=user_id, end_date=None).first()
            if open_streak:
                return None  # Open streak exists, do nothing
            streak = Streak(user_ID=user_id, start_date=check_date or date.today())
            session.add(streak)
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

    def end_streak(self, user_id: Optional[uuid.UUID] = None, close_date: date = None) -> Optional[Exception]:
        """
        End an open streak for a user.
        Returns: Error or None
        """
        if user_id is None:
            user_id = self.fixed_user_id
        session = self.Session()
        try:
            streak = session.query(Streak).filter_by(user_ID=user_id, end_date=None).first()
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

