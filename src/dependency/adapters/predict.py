import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from starlette import concurrency

from src.dependency.ports import Classifier


class IrisInferencer(Classifier):
    def __init__(self, *, model: KNeighborsClassifier | DecisionTreeClassifier) -> None:
        self.model = model

    async def predict_proba(self, *, data: pd.DataFrame) -> np.ndarray:
        res = await concurrency.run_in_threadpool(func=self.model.predict_proba, X=data)
        return res  # type: ignore
