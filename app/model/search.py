from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError

from app.model.create_db import Users, create_session
from app.model.Global import DbURL, SECRET_KEY
import app.model.error as error

class SearchMethod():
    def __init__(self):
        self.engine = create_engine()

    def
