from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Classifier(ABC):

    @abstractmethod
    async def predict_proba(self, *, data: pd.DataFrame) -> np.ndarray: ...
