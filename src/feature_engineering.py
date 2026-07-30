import pandas as pd
import os
class FeatureEngineer:
    def __init__(self,input_file,output_file):
        self.input_file=input_file
        self.output_file=output_file
    def load_data(self):
        self.df=pd.read_csv(self.input_file)
    def create_signal_quality_score(self):
        self.df["Signal_Quality_Score"]=(0.6*self.df["SINR"]+0.4*(self.df["RSRP"]+120))
    def create_network_load(self):
        MAX_USERS=200
        self.df["Network_Load"]=(self.df["Connected_Users"]/MAX_USERS)
    def create_network_health_index(self):
        self.df["Network_Health_Index"]=(self.df["Throughput"]-self.df["Latency"]-(10*self.df["Packet_Loss"]))
    def save_data(self):
        os.makedirs(os.path.dirname(self.output_file),exist_ok=True)
        self.df.to_csv(self.output_file,index=False)
        print("Feature Engineering dataset saved successfully")
    def run(self):
        self.load_data()
        self.create_signal_quality_score()
        self.create_network_load()
        self.create_network_health_index()
        self.save_data()
if __name__=="__main__":
     engineer = FeatureEngineer(input_file="data/processed/telecom_kpi_cleaned.csv",output_file="data/processed/telecom_kpi_processed.csv")
     engineer.run()