from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ..database import SessionLocal
from .. import models

router = APIRouter(prefix="/problems", tags=["problems"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TestCaseCreate(BaseModel):
    input_data: str
    expected_output: str

class ProblemCreate(BaseModel):
    title: str
    description: str
    input_example: str
    output_example: str
    test_cases: List[TestCaseCreate]

@router.post("/")
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    db_problem = models.Problem(
        title=problem.title,
        description=problem.description,
        input_example=problem.input_example,
        output_example=problem.output_example,
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)

    for case in problem.test_cases:
        test_case = models.TestCase(
            input_data=case.input_data,
            expected_output=case.expected_output,
            problem_id=db_problem.id
        )
        db.add(test_case)

    db.commit()
    return {"message": "Problem created", "problem_id": db_problem.id}

@router.get("/")
def list_problems(db: Session = Depends(get_db)):
    problems = db.query(models.Problem).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description
        }
        for p in problems
    ]

@router.get("/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        return {"error": "Not found"}

    test_cases = db.query(models.TestCase).filter(models.TestCase.problem_id == problem_id).all()

    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "input_example": problem.input_example,
        "output_example": problem.output_example,
        "test_cases": [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output
            } for tc in test_cases
        ]
    }