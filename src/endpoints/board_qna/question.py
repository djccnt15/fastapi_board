from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from settings.database import get_db
from src.models.models import Question as QuestionModel
from src.schemas.board_qna import Question

router = APIRouter(
    prefix="/api/question",
)


@router.get("/list", response_model=list[Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(QuestionModel).order_by(QuestionModel.date_create.desc()).all()
    return _question_list