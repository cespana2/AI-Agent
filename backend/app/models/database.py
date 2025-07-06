from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chunks.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TextChunk(Base):
    __tablename__ = "chunks"
    id = Column(String, primary_key=True, index=True)
    file_name = Column(String, index=True)  # Optional: to identify the source file
    content = Column(String)
    position = Column(Integer)  # Optional: which order it was in the doc
    embedding = Column(Text)  # Store the embedding as a string (or use a more complex type if needed)

# Create the table (run once at startup)
Base.metadata.create_all(bind=engine)