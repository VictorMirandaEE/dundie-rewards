"""Database module of dundie."""

from sqlmodel import Session, create_engine

from dundie import models
from dundie.settings import SQL_CONNECTION_STRING

engine = None


def get_session() -> Session:
    """
    Get a new SQLModel session object.

    This function creates and returns a new SQLModel session with the
    specified engine binding. If the engine is not already created, it
    initializes the engine using the SQL_CONNECTION_STRING and creates
    all tables defined in the models.

    Returns:
        Session: A new SQLModel session object.
    """
    global engine

    if not engine:
        engine = create_engine(SQL_CONNECTION_STRING, echo=False)
        models.SQLModel.metadata.create_all(bind=engine)

    return Session(bind=engine, autocommit=False, autoflush=False)
