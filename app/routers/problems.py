from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
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

class TestCaseUpdate(BaseModel):
    id: Optional[int] = None
    input_data: str
    expected_output: str

class ProblemCreate(BaseModel):
    title: str
    description: str
    input_example: str
    output_example: str
    test_cases: List[TestCaseCreate]
    
class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    input_example: Optional[str] = None
    output_example: Optional[str] = None
    test_cases: Optional[List[TestCaseUpdate]] = None

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

@router.delete("/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    # Primero eliminar test cases relacionados debido a restricciones de clave foránea
    db.query(models.TestCase).filter(models.TestCase.problem_id == problem_id).delete()
    
    # Luego eliminar el problema
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        return {"error": "Problem not found"}
    
    db.delete(problem)
    db.commit()
    
    return {"message": f"Problem with ID {problem_id} has been deleted"}

@router.put("/{problem_id}")
def update_problem(problem_id: int, problem_update: ProblemUpdate, db: Session = Depends(get_db)):
    # Buscar el problema existente
    db_problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not db_problem:
        return {"error": "Problem not found"}
    
    # Actualizar los campos del problema si se proporcionan
    if problem_update.title is not None:
        db_problem.title = problem_update.title
    if problem_update.description is not None:
        db_problem.description = problem_update.description
    if problem_update.input_example is not None:
        db_problem.input_example = problem_update.input_example
    if problem_update.output_example is not None:
        db_problem.output_example = problem_update.output_example
    
    # Actualizar casos de prueba si se proporcionan
    if problem_update.test_cases is not None:
        # Borrar los antiguos casos de prueba
        db.query(models.TestCase).filter(models.TestCase.problem_id == problem_id).delete()
        
        # Crear los nuevos casos de prueba
        for case in problem_update.test_cases:
            test_case = models.TestCase(
                input_data=case.input_data,
                expected_output=case.expected_output,
                problem_id=problem_id
            )
            db.add(test_case)
    
    db.commit()
    db.refresh(db_problem)
    
    return {"message": f"Problem with ID {problem_id} has been updated"}