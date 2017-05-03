from datetime import date
from flask_login import UserMixin
import werkzeug.security as ws

from sqlalchemy import Column, String, Integer, Boolean, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///KSEF-Nairobi.db")
Base.metadata.bind = engine

class Educator(Base, UserMixin):
    __tablename__ = "educators"
    id = Column(Integer, primary_key=True)
    register_as = Column(String)
    fullname = Column(String)
    email = Column(String(120), unique=True)
    password_hash = Column(String)
    county = Column(String)
    sub_county_name = Column(String)
    school = Column(String)
    is_admin = Column(Boolean, default=False)
    is_adjudicator = Column(Boolean, default=False)
    date_signedup = Column(String)
    is_approved = Column(Boolean, default=False)

    





    """def __init__(self, password, email, fullname, school):
        self.fullname = fullname
        self.email = email
        self.password_hash = ws.generate_password_hash(password)
        self.date_signedup = date.today()

    def check_password(self, password):
        return ws.check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return session.query(Teacher).filter_by(email=email).first()

    @staticmethod
    def add_user(user):
        session.add(user)
        session.commit()"""

Base.metadata.create_all(engine)
