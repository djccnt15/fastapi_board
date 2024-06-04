from pydantic import BaseModel


class IrisResponse(BaseModel):
    setosa: float
    versicolor: float
    virginica: float
