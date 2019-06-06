from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

# from app.models.user import Owner, Tenant
from app import Base

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    property_type = Column(String(20))
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship('Owner', back_populates='properties')
    tenants = relationship('Tenant', back_populates='properties')
