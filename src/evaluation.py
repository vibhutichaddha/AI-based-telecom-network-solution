import joblib
import pandas as pd
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report)
import logging
import os 
from typing import Optional
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)
class ModelEvaluation:
    REQUIRED_COLUMNS=["Actual_Label","Anomaly",]
    def __init__(self, input_file:str):
        self.input_file = input_file
        self.df:Optional[pd.DataFrame]=None
    def load_data(self)->None:
        logger.info("Loading evaluation dataset")
        try:
            self.df = pd.read_csv(self.input_file)
            logger.info("Dataset loaded successfully (%d rows)",len(self.df),)
        except FileNotFoundError:
            logger.error("Dataset not found:%s",self.input_file,)
            raise
        except Exception as error:
            logger.exception(error)
            raise
    def validate_data(self)->None:
        missing=[
            column 
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]
        if missing:
            raise ValueError(f"Missing columns:{missing}")
        logger.info("Dataset validation successful")
    def prepare_labels(self)->None:
        logger.info("Preparing Labels")
        mapping = {"Normal": 1,"Anomaly": -1,}
        self.df["Actual_Label"] = (self.df["Actual_Label"].astype(str).str.strip())
        self.df["Anomaly"] = (self.df["Anomaly"].astype(str).str.strip())
        self.y_true = self.df["Actual_Label"].map(mapping)
        self.y_pred = self.df["Anomaly"].map(mapping)
    def evaluate(self)->None:
        logger.info("Evaluating model")
        accuracy = accuracy_score(self.y_true,self.y_pred)
        precision = precision_score(self.y_true,self.y_pred,pos_label=-1)
        recall = recall_score(self.y_true,self.y_pred,pos_label=-1)
        f1 = f1_score(self.y_true,self.y_pred,pos_label=-1)
        cm=confusion_matrix(self.y_true,self.y_pred,)
        report=classification_report(self.y_true,self.y_pred,)
        logger.info("\nModel Evaluation")
        logger.info("Accuracy : %.4f",accuracy)
        logger.info("Precision: %.4f}",precision)
        logger.info("Recall: %.4f}",recall)
        logger.info("F1 Score : %.4f}",f1)
        logger.info("\nConfusion Matrix")
        print(cm)
        logger.info("\nClassification Report")
        print(report)
        self.save_report(accuracy,precision,recall,f1,cm,report,)
    def save_report(self,accuracy,precision,recall,f1,cm,report,)->None:
        os.makedirs("reports",exist_ok=True)
        with open("reports/model_evaluation.txt","w",) as file:
            file.write("MODEL EVALUATION REPORT\n")
            file.write(f"Accuracy:{accuracy:.4f}\n")
            file.write(f"Precision:{precision:.4f}\n")
            file.write(f"Recall:{recall:.4f}\n")
            file.write(f"F1 Score:{f1:.4f}\n\n")
            file.write("Confusion Matrix\n")
            file.write(str(cm))
            file.write(report)
        logger.info("Evaluation report saved to reports/model_evaluation.txt")
    def run(self)->None:
        self.load_data()
        self.validate_data()
        self.prepare_labels()
        self.evaluate()
def main()->None:
    evaluator=ModelEvaluation("data/processed/telecom_kpi_with_anomalies.csv")
    evaluator.run()
if __name__ == "__main__":
    main()