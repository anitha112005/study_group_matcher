import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import json
from contextlib import contextmanager

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gpa = Column(Float, default=0.0)
    courses = Column(JSON, default=[])
    availability = Column(JSON, default=[])  # e.g. ["Mon 18:00-20:00", "Wed 10:00-12:00"]
    notes = Column(String, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gpa": self.gpa,
            "courses": self.courses or [],
            "availability": self.availability or [],
            "notes": self.notes or ""
        }

def get_engine(db_path="students.db"):
    return create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

def init_db(db_path="students.db"):
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)

def SessionLocal(db_path="students.db"):
    engine = get_engine(db_path)
    return sessionmaker(bind=engine)()

@contextmanager
def session_scope(db_path="students.db"):
    Session = sessionmaker(bind=get_engine(db_path))
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def load_sample_students(db_path="students.db", overwrite=False):
    # sample dataset
    sample = [
        { "id": 1, "name": "Alice", "gpa": 8.6, "courses": ["CS101","MATH201"], "availability": ["Mon 18:00-20:00","Wed 10:00-12:00"], "notes": "Prefers project work" },
        { "id": 2, "name": "Bob", "gpa": 7.8, "courses": ["CS101","PHY101"], "availability": ["Mon 18:00-20:00","Tue 14:00-16:00"], "notes":"Good at algorithms" },
        { "id": 3, "name": "Carol", "gpa": 9.0, "courses": ["MATH201","STAT101"], "availability": ["Wed 10:00-12:00","Thu 16:00-18:00"], "notes": "Looks for tutoring" },
        { "id": 4, "name": "Dan", "gpa": 8.0, "courses": ["CS101","MATH201"], "availability": ["Mon 18:00-20:00","Thu 16:00-18:00"], "notes": "Team player" },
        { "id": 5, "name": "Eve", "gpa": 6.9, "courses": ["PHY101","STAT101"], "availability": ["Tue 14:00-16:00","Thu 16:00-18:00"], "notes": "" }
    ]
    engine = get_engine(db_path)
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        if overwrite:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
        # Only insert if table empty
        if session.query(Student).count() == 0:
            for s in sample:
                student = Student(id=s["id"], name=s["name"], gpa=s["gpa"], courses=s["courses"], availability=s["availability"], notes=s.get("notes",""))
                session.add(student)
            session.commit()
    finally:
        session.close()
