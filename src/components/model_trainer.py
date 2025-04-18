import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
#from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts", "model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_arr, test_arr):
        try:
            logging.info("Entered the model training method or component")
            logging.info("Model training initiated")
            X_train,X_test,y_train,y_test= (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
                )

            models = { "Random Forest": RandomForestRegressor(),
            "Decision Tree": DecisionTreeRegressor(),
            "Gradient Boosting": GradientBoostingRegressor(),
            "Linear Regression": LinearRegression(),
            "CatBoosting Regressor": CatBoostRegressor(verbose=False),
            "AdaBoost Regressor": AdaBoostRegressor(),
                
            }
                
            params = { "Decision Tree": {"max_depth": [2, 3, 4, 5, 6]},
            "Random Forest": {"n_estimators": [100, 200, 300, 400, 500]},
            "Gradient Boosting": {"n_estimators": [100, 200, 300, 400, 500]},
            "Linear Regression": {},
            "CatBoosting Regressor": {"iterations": [100, 200, 300, 400, 500]},
            "AdaBoost Regressor": {"n_estimators": [100, 200, 300, 400, 500]},
                
            }

            model_report = evaluate_models( X_train, y_train, X_test, y_test, models, params)
            logging.info("Model training completed")

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
              list(model_report.values()).index(best_model_score)
               ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.model_path,
                obj=best_model
                )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square
            
        except Exception as e:
            raise CustomException(e,sys)