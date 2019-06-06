from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.property import Property

from app import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))
    password_hash = Column(String(128))
    tenant = relationship('Tenant', back_populates='user')
    owner = relationship('Owner', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    property_id = Column(Integer, ForeignKey('properties.id'))
    user = relationship('User', back_populates='tenant')
    properties = relationship('Property', back_populates='tenants')

class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='owner')
    properties = relationship('Property', back_populates='owner')
    
