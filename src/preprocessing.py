"""
Telecom Data Preprocessing Module

This module loads, validates, cleans and saves 
telecom KPI datasets for the Telecom AI Capstone Project"""
import os
import pandas as pd
import logging
from typing import Optional 
logging.basicConfig(level=logging.INFO,format="%(asctime)s-%(levelname)s-%(message)s")
logger=logging.getLogger(__name__)
class TelecomDataPreprocessor:
    """
    A class to preprocess telecom KPI datasets
    
    Attributes:
        input_file(str): Path to the raw dataset
        output_file(str): Path to save the cleaned dataset
        df (pd.DataFrame): Loaded Dataset
    """
    REQUIRED_COLUMNS = ["Timestamp","Cell_ID","RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users"]
    OPTIONAL_COLUMNS = ["Site_ID","Network_Status"]
    NUMERIC_COLUMNS=["RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users"]
    def __init__(self,input_file:str,output_file:str):
        self.input_file=input_file
        self.output_file=output_file
        self.df:Optional[pd.DataFrame]=None 
    def load_data(self)->None:
        logger.info("Loading dataset")
        try:
            self.df=pd.read_csv(self.input_file)
            logger.info("Dataset loaded successfully")
        except FileNotFoundError:
            logger.error("Input dataset not found")
            raise
        except pd.errors.EmptyDataError:
            logger.error("Dataset is empty")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            raise  
    def validate_data(self)->None:
        logger.info("Validating dataset")
        if self.df is None:
            raise ValueError("Dataset has not been loaded")
        missing_required = [
            column 
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
            ]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
        missing_optional = [
            column 
            for column in self.OPTIONAL_COLUMNS
            if column not in self.df.columns
            ]
        if missing_optional: 
            logger.warning("Optional Columns Missing: %s",missing_optional)
        logger.info("Dataset validation successful")
        logger.info("Data Types:\n%s",self.df.dtypes)
        logger.info("Missing Values:\n%s",self.df.isnull().sum())
    def fill_missing_values(self)->None:
        for column in self.NUMERIC_COLUMNS:
            self.df[column]=self.df[column].fillna(self.df[column].median())
    def remove_duplicates(self)->None:
        self.df.drop_duplicates(inplace=True)
    def remove_invalid_rows(self)->None:
        self.df=self.df[self.df["Latency"]>=0]
        self.df=self.df[self.df["Packet_Loss"]>=0]
        self.df=self.df[self.df["Connected_Users"]>=0]
    def convert_timestamp(self)->None:
        self.df["Timestamp"]=pd.to_datetime(self.df["Timestamp"],errors="coerce")
        self.df.dropna(subset=["Timestamp"],inplace=True)
    def clean_data(self)->None:
        logger.info("Cleaning dataset")
        if self.df is None:
            raise ValueError("Dataset has not been loaded")
        self.fill_missing_values
        self.remove_duplicates
        self.remove_invalid_rows
        self.convert_timestamp
        logger.info("Dataset Cleaned Successfully")
    def save_data(self)->None:
        logging.info("Saving cleaned dataset")
        if self.df is None:
            raise ValueError("No dataset available to save")
        os.makedirs(os.path.dirname(self.output_file),exist_ok=True)
        self.df.to_csv(self.output_file,index=False)
        logger.info("Processed dataset saved to %s", self.output_file)
def main()->None:
    processor=TelecomDataPreprocessor(input_file="data/raw/telecom_kpi_balanced.csv",output_file="data/processed/telecom_kpi_cleaned.csv",)
    processor.load_data()
    processor.validate_data()
    processor.clean_data()
    processor.save_data()
if __name__=="__main__":
    main()