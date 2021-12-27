from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from passlib.context import CryptContext

from app.database import Base, db_context

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ModelUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String(255))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    @staticmethod
    def get_user_by_username(username):
        with db_context() as session:
            return session.query(ModelUser).filter(ModelUser.name == username).first()

