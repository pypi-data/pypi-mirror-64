import functools
import os
from contextlib import contextmanager

from littleutils import retry
from sqlalchemy import create_engine, Column, Text, DateTime, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import InterfaceError, OperationalError, InternalError, ProgrammingError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

url = "postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(
    **os.environ)
engine = create_engine(
    url,
    # echo=True,
)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__dict__.get("__name__", cls.__name__).lower()


Base = declarative_base(cls=Base)


class WithAutoKey:
    id = Column("id", Integer, primary_key=True)


class ComposerQuery(Base, WithAutoKey):
    client_id = Column(Text)
    user = Column(Text)
    results = Column(LargeBinary)
    parameters = Column(JSON)
    composer = Column(JSON)
    timestamp = Column(DateTime)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# Based on https://docs.sqlalchemy.org/en/latest/errors.html#error-dbapi
retry_db = retry(3, (InterfaceError, OperationalError, InternalError, ProgrammingError))


def provide_session(func):
    @retry_db
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with session_scope() as session:
            return func(self, session, *args, **kwargs)

    return wrapper
