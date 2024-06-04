import numpy as np
import pandas as pd

from ..model import predict_request, predict_response


async def iris_to_df(*, data: predict_request.IrisRequest) -> pd.DataFrame:
    df = pd.DataFrame(data=[data.model_dump()])
    return df


async def iris_to_response(*, data: np.ndarray) -> predict_response.IrisResponse:
    record = data[0]
    res = predict_response.IrisResponse(
        setosa=record[0],
        versicolor=record[1],
        virginica=record[2],
    )
    return res
