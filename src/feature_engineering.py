import pandas as pd
import logging
from typing import Optional
import os
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)
class FeatureEngineer:
    MAX_USERS=200
    REQUIRED_COLUMNS=["RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users"]
    def __init__(self,input_file:str,output_file:str):
        self.input_file=input_file
        self.output_file=output_file
        self.df:Optional[pd.DataFrame]=None 
    def load_data(self)->None:
        logger.info("Loading cleaned dataset")
        try:
            self.df=pd.read_csv(self.input_file)
            logger.info("Dataset loaded successfully")
        except FileNotFoundError:
            logger.error("Input dataset not found")
            raise
        except Exception as error:
            logger.exception(f"Unexpected error: {error}")
            raise
    def validate_dataset(self)->None:
        if self.df is None:
            raise ValueError("Dataset has not been loaded")
        missing_columns = [
            column 
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
            ]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        logger.info("Dataset Validation Successful")
    def create_signal_quality_score(self)->None:
        logger.info("Creating Signal Quality Score")
        self.df["Network_Load"]=(self.df["Connected_Users"]/self.MAX_USERS)
    def create_network_load(self)->None:
        logger.info("Creating Network Health Index")
        self.df["Network_Health_Index"]=(self.df["Throughput"]-self.df["Latency"]-(10*self.df["Packet_Loss"]))
    def create_network_health_index(self)->None:
        logger.info("Creating Network Health Index")
        self.df["Network_Health_Index"] = (self.df["Throughput"]- self.df["Latency"]- (10 * self.df["Packet_Loss"]))
    def save_data(self)->None:
        logger.info("Saving processed dataset")
        if self.df is None:
            raise ValueError ("No dataset available to save")
        os.makedirs(os.path.dirname(self.output_file),exist_ok=True)
        self.df.to_csv(self.output_file,index=False)
        logger.info("Feature engineered dataset saved to %s", self.output_file)
    def run(self)->None:
        self.load_data()
        self.validate_dataset()
        self.create_signal_quality_score()
        self.create_network_load()
        self.create_network_health_index()
        self.save_data()
        logger.info("Feature engineering completed successfully")
def main()->None:
     engineer = FeatureEngineer(input_file="data/processed/telecom_kpi_cleaned.csv",output_file="data/processed/telecom_kpi_processed.csv",)
     engineer.run()
if __name__ == "__main__":
    main()