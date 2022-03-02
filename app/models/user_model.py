from app.configs.database import db
from sqlalchemy import Column, Integer, VARCHAR
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass

@dataclass
class UserModel(db.Model):
    name: str
    last_name: str
    email: str

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(127), nullable=False)
    last_name = Column(VARCHAR(511), nullable=False)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    password_hash = Column(VARCHAR(511), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not accessible")
    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)
    
    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)