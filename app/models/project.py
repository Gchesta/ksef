from datetime import date
import werkzeug.security as ws

from sqlalchemy import Column, String, Integer, Boolean, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///KSEF-Nairobi.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    title = Column(String(120))
    category = Column(String(120))
    first_presenter = Column(String(120))
    second_presenter = Column(String(120))
    is_presented = Column(Boolean, default=False)
    first_adjudicator = Column(String(120))
    second_adjudicator = Column(String(120))
    third_adjudicator = Column(String(120))
    school = Column(String(120))
    number_of_adjudicators = Column(Integer)
    first_score = Column(Integer)
    second_score = Column(Integer)
    third_score = Column(Integer)
    aggregate_score = Column(Integer)
    average_score = Column(Float)
    date_registered = Column(String)
    date_presented = Column(String)

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(120))



Base.metadata.create_all(engine)
