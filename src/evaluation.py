import joblib
import pandas as pd
from sklearn.metrics import (accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report)
class ModelEvaluation:
    def __init__(self, input_file):
        self.input_file = input_file
    def load_data(self):
        print("Loading dataset")
        self.df = pd.read_csv(self.input_file)
    def prepare_labels(self):
        self.y_true = self.df["Actual_Label"]
        self.y_pred = self.df["Anomaly"]
        self.y_true = self.y_true.map({"Normal": 1,"Anomaly": -1})
        self.y_pred = self.y_pred.map({"Normal": 1,"Anomaly": -1})
    def evaluate(self):
        accuracy = accuracy_score(self.y_true,self.y_pred)
        precision = precision_score(self.y_true,self.y_pred,pos_label=-1)
        recall = recall_score(self.y_true,self.y_pred,pos_label=-1)
        f1 = f1_score(self.y_true,self.y_pred,pos_label=-1)
        print("\nModel Evaluation")
        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print("\nConfusion Matrix")
        print(confusion_matrix(self.y_true,self.y_pred))
        print("\nClassification Report")
        print(classification_report(self.y_true,self.y_pred))
if __name__ == "__main__":
    evaluator = ModelEvaluation("data/processed/telecom_kpi_with_anomalies.csv")
    evaluator.load_data()
    evaluator.prepare_labels()
    evaluator.evaluate()