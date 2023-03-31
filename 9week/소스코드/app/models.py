from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), unique=True, index=True)
    salt = Column(String(length=128))
    password = Column(String(length=128))

    pastes = relationship('Paste', back_populates='owner')


class Paste(Base):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True, index=True)
    # Paste 모델을 구현하는 부분입니다.
    # 과제에서 요구하는 title과 content를 추가해주었습니다.
    title = Column(String(length=128))
    content = Column(String(length=128))
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='pastes')
