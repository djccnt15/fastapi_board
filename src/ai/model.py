import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from src.core.configs import RESOURCES
from src.domain.predict.model.enums.predict_enum import AlgorithmEnum

AI_MODEL_PATH = RESOURCES / "ai_model"

iris_classifier: dict[AlgorithmEnum, KNeighborsClassifier | DecisionTreeClassifier] = {}


def load_ml_models():
    iris_classifier[AlgorithmEnum.DT] = joblib.load(
        filename=AI_MODEL_PATH / "dt.joblib"
    )
    iris_classifier[AlgorithmEnum.KNN] = joblib.load(
        filename=AI_MODEL_PATH / "knn.joblib"
    )


def clear_resource():
    iris_classifier.clear()
