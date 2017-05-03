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

class SubCounty(Base):
    __tablename__ = "sub_counties"
    sub_county_id = Column(Integer, primary_key=True)
    sub_county_name = Column(String(120))
    
    @staticmethod
    def add_zone(zone):
        session.add(zone)
        session.commit()

class School(Base):
    __tablename__ = "schools"
    school_id = Column(Integer, primary_key=True)
    sub_county_name = Column(String(120))
    school_name = Column(String(120))
    
    @staticmethod
    def add_school(school):
        session.add(school)
        session.commit()
    
    

Base.metadata.create_all(engine)