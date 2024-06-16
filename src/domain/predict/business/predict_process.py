from src.dependency import ports

from ..converter import predict_converter
from ..model import predict_request, predict_response


async def predict_iris(
    *,
    inferencer: ports.Classifier,
    data: predict_request.IrisRequest,
) -> predict_response.IrisResponse:
    df = await predict_converter.iris_to_df(data=data)
    proba = await inferencer.predict_proba(data=df)
    res = await predict_converter.iris_to_response(data=proba)
    return res
