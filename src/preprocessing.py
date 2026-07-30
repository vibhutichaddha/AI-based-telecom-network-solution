import os
import pandas as pd
class TelecomDataPreprocessor:
    def __init__(self,input_file,output_file):
        self.input_file=input_file
        self.output_file=output_file
    def load_data(self):
        print("Loading dataset")
        self.df=pd.read_csv(self.input_file)
        print("Dataset loaded successfully")
        return self.df
    def validate_data(self):
        print("\nValidating dataset...")
        required_columns = ["Timestamp","Cell_ID","RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users"]
        optional_columns = ["Site_ID","Network_Status"]
        missing_required = [
            col for col in required_columns
            if col not in self.df.columns
            ]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
        missing_optional = [
            col for col in optional_columns
            if col not in self.df.columns
            ]
        if missing_optional:
            print(f"Warning: Optional columns not found: {missing_optional}")
            print("Dataset validation successful.")
            print("\nData Types")
            print(self.df.dtypes)
            print("\nMissing Values")
            print(self.df.isnull().sum())
    def clean_data(self):
        print("\nCleaning dataset")
        numerical_columns=["RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users"]
        for col in numerical_columns:
            self.df[col]=self.df[col].fillna(self.df[col].median())
        self.df.drop_duplicates(inplace=True)
        self.df=self.df[self.df["Latency"]>=0]
        self.df=self.df[self.df["Packet_Loss"]>=0]
        self.df=self.df[self.df["Connected_Users"]>=0]
        self.df["Timestamp"]=pd.to_datetime(self.df["Timestamp"])
        print("Cleaning Completed")
    def save_data(self):
        os.makedirs(os.path.dirname(self.output_file),exist_ok=True)
        self.df.to_csv(self.output_file,index=False)
        print(f"\nProcessed dataset saved to\n {self.output_file}")
if __name__=="__main__":
    processor=TelecomDataPreprocessor(input_file="data/raw/telecom_kpi_balanced.csv",output_file="data/processed/telecom_kpi_cleaned.csv")
    processor.load_data()
    processor.validate_data()
    processor.clean_data()
    processor.save_data()