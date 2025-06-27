import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text,Integer,Boolean,DateTime
from .database import Base


class Paste(Base):
    __tablename__ = "pastes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(10), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_in = Column(Integer, nullable=True)  # seconds
    is_active = Column(Boolean, default=True)