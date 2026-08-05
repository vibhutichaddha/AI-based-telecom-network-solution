import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging
from typing import Optional 
import os 
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",)
logger = logging.getLogger(__name__)
class HyperparameterTuner:
    FEATURES=["RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users","Network_Load","Network_Health_Index"]
    ESTIMATORS=[50,100,200]
    CONTAMINATION_VALUES=[0.01,0.03,0.05,0.10]
    def __init__(self,input_file:str):
        self.input_file=input_file
        self.df: Optional[pd.DataFrame]=None
    def load_data(self)->None:
        logger.info("Loading dataset")
        try:
            self.df=pd.read_csv(self.input_file)
            logger.info("Dataset loaded successfully")
        except Exception as error:
            logger.exception(error)
            raise
    def prepare_features(self)->None:
        missing=[
            column
            for column in self.FEATURES
            if column not in self.df.columns
        ]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        X=self.df[self.FEATURES]
        scaler=StandardScaler()
        self.X_scaled=scaler.fit_transform(X)
    def tune(self)->None:
        logger.info("Starting Hyperparameter Tuning")
        results=[]
        for trees in self.ESTIMATORS:
            for contamination in self.CONTAMINATION_VALUES:
                logger.info("Trees=%d Contamination=%.2f",trees,contamination)
                model=IsolationForest(n_estimators=trees,contamination=contamination,random_state=42)
                predictions=model.fit_predict(self.X_scaled)
                anomaly_count=(predictions==-1).sum()
                anomaly_percentage=(anomaly_count/len(predictions))*100
                results.append({"Trees":trees,"Contamination":contamination,"Detected_Anomalies":anomaly_count,"Anomaly_Percentage":round(anomaly_percentage,2,),})
        self.results_df=pd.DataFrame(results)
    def save_results(self)->None:
        os.makedirs("reports",exist_ok=True)
        output_path=("reports/hyperparameter_tuning.csv")
        self.results_df.to_csv(output_path,index=False,)
        logger.info("Results saved to %s",output_path,)
        logger.info("\n%s",self.results_df)
    def run(self)->None:
        self.load_data()
        self.prepare_features()
        self.tune()
        self.save_results()
def main()->None:
    tuner=HyperparameterTuner("data/processed/telecom_kpi_processed.csv")
    tuner.run()
if __name__=="__main__":
    main()