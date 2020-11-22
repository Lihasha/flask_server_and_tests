from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload

engine = create_engine("postgresql://postgres:postgres@postgres:5432/results", echo=True)

Base = declarative_base()


class Test(Base):
    __tablename__ = "test-table"
    key = Column(String, primary_key=True)
    value = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_key_and_value(key, value):
    if bool(session.query(Test).filter_by(key=key).first()):
        raise ValueError("Already existing key")
    new_kv = Test(key=key, value=value)
    session.add(new_kv)
    session.commit()


def return_value_from_key(key):
    if not bool(session.query(Test).filter_by(key=key).first()):
        raise ValueError("No such key")
    return session.query(Test).filter_by(key=key).first().value
