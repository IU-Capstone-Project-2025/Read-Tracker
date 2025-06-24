from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
import models

engine = create_engine(
    url="postgresql://postgres:password@database:5432/reader_library_db",
    echo=False
)

models.Base.metadata.create_all(engine)

