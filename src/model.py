import os
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
class TelecomAnomalyModel:
    def __init__(self,input_file):
        self.input_file=input_file
    def load_data(self):
        print("LOading processed dataset")
        self.df=pd.read_csv(self.input_file)
    def prepare_features(self):
        features=["RSRP","SINR","Throughput","Latency","Packet_Loss","Connected_Users","Signal_Quality_Score","Network_Load","Network_Health_Index"]
        self.X=self.df[features]
    def scale_data(self):
        self.scaler=StandardScaler()
        self.X_scaled=self.scaler.fit_transform(self.X)
    def train_model(self):
        print("Training Isolation Forest")
        self.model=IsolationForest(n_estimators=100,contamination=0.05,random_state=42)
        self.model.fit(self.X_scaled)
    def predict(self):
        predictions=self.model.predict(self.X_scaled)
        self.df["Anomaly"]=predictions
        self.df["Anomaly"]=self.df["Anomaly"].map({1:"Normal",-1:"Anomaly"})
    def save_model(self):
        os.makedirs("models",exist_ok=True)
        joblib.dump(self.model,"models/isolation_forest.pkl")
        joblib.dump(self.scaler,"models/scaler.pkl")
        self.df.to_csv("data/processed/telecom_kpi_with_anomalies.csv",index=False)
        print("Model saved successfully")
    def run(self):
        self.load_data()
        self.prepare_features()
        self.scale_data()
        self.train_model()
        self.predict()
        self.save_model()
if __name__=="__main__":
    model=TelecomAnomalyModel("data/processed/telecom_kpi_processed.csv")
    model.run()