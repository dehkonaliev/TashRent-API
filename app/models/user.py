from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Enum, String, func, text

from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class UserRole(StrEnum):
    USER = 'user'
    LANDLORD = 'landlord'
    ADMIN = 'admin'
    
    
class User(Base):
    __tablename__='users'
    
    