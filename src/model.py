import os
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging
from typing import Optional
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)
class TelecomAnomalyModel:
    FEATURES = ["RSRP","SINR","Throughput","Latency","Packet_Loss","Connected_Users","Network_Load","Network_Health_Index",]
    def __init__(self,input_file:str):
        self.input_file=input_file
        self.df: Optional[pd.DataFrame] = None
        self.model: Optional[IsolationForest] = None
        self.scaler: Optional[StandardScaler] = None
    def load_data(self)->None:
        logger.info("Loading processed dataset")
        try:
            self.df=pd.read_csv(self.input_file)
            logger.info("Dataset loaded successfully")
        except FileNotFoundError():
            logger.error("Dataset not found: %s",self.input_file)
            raise
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")
            raise
        logger.info("Columns in dataset:")
        logger.info(self.df.columns.tolist())
    def prepare_features(self)->None:
        logger.info("Preparing features")
        missing_columns = [
            column 
            for column in self.FEATURES
            if column not in self.df.columns
            ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        self.X=self.df[self.FEATURES]
    def scale_data(self)->None:
        logger.info("Scaling Features")
        self.scaler=StandardScaler()
        self.X_scaled=self.scaler.fit_transform(self.X)
    def train_model(self)->None:
        logger.info("Training Isolation Forest Model")
        self.model=IsolationForest(n_estimators=100,contamination=0.05,random_state=42)
        self.model.fit(self.X_scaled)
        logger.info("Model training completed")
    def predict(self)->None:
        logger.info("Generating predictions")
        predictions=self.model.predict(self.X_scaled)
        self.df["Anomaly"]=predictions
        self.df["Anomaly"]=self.df["Anomaly"].map({1:"Normal",-1:"Anomaly"})
        anomaly_count=(self.df["Anomaly"]=="Anomaly").sum()
        logger.info("Detected %d Anomalies",anomaly_count,)
    def save_model(self)->None:
        logger.info("Saving model and output files")
        os.makedirs("models",exist_ok=True)
        os.makedirs("data/processed",exist_ok=True)
        joblib.dump(self.model,"models/isolation_forest.pkl")
        joblib.dump(self.scaler,"models/scaler.pkl")
        self.df.to_csv("data/processed/telecom_kpi_with_anomalies.csv",index=False)
        logger.info("Model and processed dataset saved successfully")
    def run(self):
        logger.info("Starting anomaly detection pipeline")
        self.load_data()
        self.prepare_features()
        self.scale_data()
        self.train_model()
        self.predict()
        self.save_model()
        logger.info("Pipeline completed successfully")
def main()->None:
    model=TelecomAnomalyModel("data/processed/telecom_kpi_processed.csv")
    model.run()
if __name__=="__main__":
    main()