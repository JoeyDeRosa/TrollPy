from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Boolean
)

from .meta import Base
from passlib.apps import custom_app_context as pwd_context


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, unique=True)
    password = Column(Unicode)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    email = Column(Unicode, unique=True)
    board = Column(Unicode)
    winner = Column(Unicode)
    in_check = Column(Boolean)
    trollspeak = Column(Unicode)
    admin = Column(Boolean)

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = pwd_context.hash(kwargs['password'])
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.email = kwargs['email']
        self.board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.winner = 'None'
        self.in_check = False
        self.trollspeak = 'Prepare to die.'
        self.admin=kwargs['admin']

    def to_json(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "board": self.board,
            "winner": self.winner,
            "in_check": self.in_check,
            "trollspeak": self.trollspeak
            }


class KillScore(Base):
    __tablename__ = 'killscore'
    id = Column(Integer, primary_key=True)
    killscore_id = Column(Integer)
    statement = Column(Unicode, unique=True)

    def __init__(self, **kwargs):
        self.killscore_id = kwargs['killscore_id']
        self.statement = kwargs['statement']

    def to_json(self):
        return {
            "id": self.id,
            "killscore_id": self.killscore_id,
            "statement": self.statement
            }
