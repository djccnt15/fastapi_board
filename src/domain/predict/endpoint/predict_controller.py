from typing import Annotated

from fastapi import APIRouter, Body

from src import dependency

from ..business import predict_process
from ..model import predict_request, predict_response

router = APIRouter(prefix="/predict")


@router.post(path="/iris")
async def predict_iris(
    inferencer: dependency.IrisInferencer,
    body: Annotated[predict_request.IrisRequest, Body()],
) -> predict_response.IrisResponse:
    """
    - algorithm: choose algorithm for inference
        - knn: k-nearest neighbors vote classifier
        - dt: decision tree classifier
    """
    res = await predict_process.predict_iris(inferencer=inferencer, data=body)
    return res
