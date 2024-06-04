import numpy as np

from src.ai import model

from ..converter import predict_converter
from ..model import predict_request, predict_response
from ..model.enums.predict_enum import AlgorithmEnum


async def predict_iris(
    *,
    algorithm: AlgorithmEnum,
    data: predict_request.IrisRequest,
) -> predict_response.IrisResponse:
    df = await predict_converter.iris_to_df(data=data)
    proba: np.ndarray = model.iris_classifier[algorithm].predict_proba(df)  # type: ignore
    res = await predict_converter.iris_to_response(data=proba)
    return res
