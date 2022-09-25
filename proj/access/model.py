from sqlalchemy import Boolean, Column,Integer, String, DateTime, ForeignKey 
from sqlalchemy.orm import relationship
from proj.access.database import Base

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String,nullable=False)
    content = Column(String, nullable=False)
    rated_18 = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default='now()', nullable=False) 
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False )
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable='False')
    email = Column(String, unique=True, index=True, nullable='False')  
    password = Column(String, nullable='False')
    is_active = Column(Boolean, server_default="False")    
    created_at = Column(DateTime(timezone=True), server_default='now()', nullable=False) 



  