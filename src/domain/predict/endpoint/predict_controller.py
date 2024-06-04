from fastapi import APIRouter

from ..business import predict_process
from ..model import predict_request, predict_response
from ..model.enums import predict_enum

router = APIRouter(prefix="/predict")


@router.post(path="/iris")
async def predict_iris(
    algorithm: predict_enum.AlgorithmEnum,
    body: predict_request.IrisRequest,
) -> predict_response.IrisResponse:
    """
    - algorithm: choose algorithm for inference
        - knn: k-nearest neighbors vote classifier
        - dt: decision tree classifier
    """
    res = await predict_process.predict_iris(algorithm=algorithm, data=body)
    return res
