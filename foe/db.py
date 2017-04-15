
"""
"""

# Native
import os
import time
from contextlib import contextmanager

# 3rd-Party
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

# Proprietary
from models.model import Model, Base


engine = create_engine('sqlite:///foe.db')


session = scoped_session(sessionmaker(autocommit=False, bind=engine))

def init():
    """
    Initalizes the database, creating all the required tables
    """

    Base.metadata.create_all(bind=engine)

def exists():
    """
    Returns True if the database has been setup (contains tables)
    """

    meta = MetaData(engine)
    meta.reflect()

    return bool(meta.tables)

def delete():
    """
    Deletes all data from the database
    """

    meta = MetaData(engine)
    meta.reflect()

    for table in reversed(meta.sorted_tables):
        engine.execute(table.delete())

def tables():
    """
    Returns a dict of all the tables in the database
    """

    meta = MetaData(engine)
    meta.reflect()

    return meta.tables

def drop():
    """
    Drops the database, essentially wiping it clean of data and tables
    """

    # Fetches the meta data (tables/schema/etc) from the database and then drops it that way,
    # rather than getting the meta data from the python classes which could leave things around
    # Or: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/DropEverything
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()
