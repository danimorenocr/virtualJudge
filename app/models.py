from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    input_example = Column(Text)
    output_example = Column(Text)
    test_cases = relationship("TestCase", back_populates="problem")

class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True)
    input_data = Column(Text)
    expected_output = Column(Text)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    problem = relationship("Problem", back_populates="test_cases")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    code = Column(Text)
    language = Column(String)
    problem_id = Column(Integer)
    result = Column(String)
    submitted_at = Column(DateTime, default=datetime.utcnow)
