from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
import database.models

# postgresql://postgres:password@database:5432/reader_library_db

engine = create_engine(
    url="postgresql://postgres:password@database:5432/reader_library_db",
    echo=False
)

database.models.Base.metadata.create_all(engine)

