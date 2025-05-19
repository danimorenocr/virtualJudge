from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, judge

router = APIRouter(prefix="/submit", tags=["submissions"])

class SubmissionRequest(BaseModel):
    code: str
    language: str
    problem_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
@router.post("/")
def submit_code(sub: SubmissionRequest, db: Session = Depends(get_db)):
    result = judge.evaluate(sub.code, sub.language, sub.problem_id, db)

    submission = models.Submission(
        code=sub.code,
        language=sub.language,
        problem_id=sub.problem_id,
        result=result["result"]  
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)


    return result
