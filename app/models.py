from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils import ValidationError, BaseClass
from app import Base


class User(Base, BaseClass):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    tenant = relationship("Tenant", back_populates="user")
    owner = relationship("Owner", back_populates="user")

    def set_password(self, password):
        if len(password) < 5:
            raise ValidationError("Password must be greater than 5")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Tenant(Base, BaseClass):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    user = relationship("User", back_populates="tenant")
    properties = relationship("Property", back_populates="tenants")


class Owner(Base, BaseClass):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="owner")
    properties = relationship("Property", back_populates="owner")


class Property(Base, BaseClass):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    property_name = Column(String(20))
    location = Column(String(20))
    property_type = Column(String(20), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    owner = relationship("Owner", back_populates="properties")
    tenants = relationship("Tenant", back_populates="properties")
