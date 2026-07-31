# AI-Based 5G KPI Anomaly Detection Dashboard
## Overview
The AI Based 5G KPI Anomaly Detection Dashboard is a machine learning project developed as part of the Week 7 capstone project. The objective is to automatically identify abnormal patterns in telecom network Key Performance Indicator (KPI) data using the Isolation Forest algorithm and present the results through an interactive Streamlit dasboard.
The project follows a complete machine learning workflow including data preprocessing, feature engineering, model training, evaluation, hyperparameter tuning, and dashboard development.
## Problem Statement
Telecommunication networks generate a massive amount of KPI data every minute from thousands of cell towers. Monitoring this data manually is inefficent and may delay the identification of faults, resulting in degraded network performance and poor user experience.
This project aims to automate anomaly detection in telecom KPIs using Artificial Intelligence, enabling network engineers to detect abnormal network behavior quickly and take corrective action.
## Project Objectives
- Clean and preprocess telecom KPI data
- Perform feature engineering to improve model performance
- Detect anomalies using the Isolation Forest algorithm
- Tune model hyperparameters
- Evaluate anomaly detection results
- Build an interactive Streamlit dashboard
- Visualize KPI trends and network health
- Provide a scalable framework for telecom network monitoring
## Technologies Used
- Python 3.12
- Pandas
- NumPy
- Scikit-Learn
- Isolation Forest
- Streamlit
- Plotly
- Matplotlib
- Joblib
- Git and GitHub
## Project Structure
```AI-Based-5G-KPI-Anomaly-Detection Dasboard
│
├── data/
│ ├── raw/
│ │    └── telecom_kpi.csv
│ └── processed/
│        ├── telecom_kpi_cleaned.csv 
│        ├── telecom_kpi_processed.csv 
│        └── telecom_kpi_with_anomalies.csv
│
├── notebooks/
│ ├── eda.ipynb
│ ├── model_training.ipynb
│ └── evaluation.ipynb
│
├── src/
│ ├── preprocessing.py
│ ├── feature_engineering.py
│ ├── model.py
│ ├── inference.py
│ ├── dashboard.py
│ └── utils.py
│
├── models/
│
├── reports/
│ ├── proposal.pdf
│ ├── evaluation.pdf
│ └── final_report.pdf
│
├── app/
│ └── streamlit_app.py
│
├── requirements.txt
├── README.md
└── .gitignore```
## Dataset Description
The project uses a telecom KPI dataset containing network performance metrics collected from multiple 5G cell sites
### Dataset Features
**Feature**       |        **Description**
Cell_ID           |       Cell Tower Identifier 
Timestamp         |       KPI Collection Time 
RSRP              |       Reference Signal Received Power
SINR              |       Signal-to-Interference-plus-Noise RATIO
Latency           |       Network Delay 
Throughput        |       Data Transmission Speed
Packet_Loss       |       Percentage of Lost Packets
Connected_Users   |       Number of Active Users
#### Engineered Features
- Signal_Quality_Score
- Network_Load
- Network_Health_Index
## Project Workflow
```Raw KPI Dataset
|
▼
Data Preprocessing
|
▼
Feature Engineering
|
▼
Feature Scaling
|
▼
Isolation Forest Model
|
▼
Anomaly Detection
|
▼
Model Evaluation
|
▼
Hyperparameter Tuning
|
▼
Streamlit Dasboard```
## Machine Learning Model
### Algorithm
Isolation Forest
### Why Isolation Forest?
- Unsupervised anomaly detection algorithm 
- Does not require labeled training data
- Efficient on large datasets
- Suitable for high-dimensional telecom KPI data
- Detects abnormal observations by isolating outliers
### Model Configuration
**Parameter**      |        **Value**
n_estimators       |          100
contamination      |          0.05
random_state       |           42
## Hyperparameter Tuning
- The following parameters were evaluated:
    - Number of Trees (n_estimators)
    - Contamination Rate
- The final configuration selected
    - n_estimators=100
    - contamination=0.05
    - random_state=42
- Results are stores in: "reports/hyperparameter_results.csv"
## Model Evaluation
The trained model was evaluated by analyzing the processed telecom KPI dataset.
The evaluation includes:
- Total records processed
- Normal records detected
- Anomaly records detected
- Anomaly distribution visualization
If reference labels are available, the following metrics can also be reported:
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
## Streamlit Dashboard
The dashboard provides an interactive interface for telecom KPI monitoring.
### Dashboard Features
- KPI Summary Cards
- Dataset Preview
- Throughput Trend
- Latency Trend
- SINR Distribution
- RSRP vs Throughput Scatter Plot
- Anomaly Distribution Chart
- Cell ID Filtering
- Download Results
Run the dashboard using: streamlit run app/streamlit_app.py
## Installation
- Clone the repository:
   - git clone <repository-url>
- Move into the project directory:
   - cd KPI_anomaly_detection_dashboard
- Create a virtual environment
   - python3 -m venv venv
- Activate the virtual environment
    - source venv/bin/activate
- Install the required dependencies
    - pip install -r requirements.txt
## Running the Project
- Run the modules in the following order:
    - python src/preprocessing.py
    - python src/feature_engineering.py
    - python src/model.py
    - python src/create_labels.py
    - python src/evaluation.py
    - python src/hyperparameter_tuning.py
- Finally launch the dashboard:
    - streamlit run app/streamlit_app.py
## Outputs
The project generates:
- Cleaned telecom KPI dataset
- Processed telecom KPI dataset
- Trained Isolation Forest model
- StandardScaler model
- Anomaly predictions
- Hyperparameter tuning results
- Evaluation report
- Streamlit dashboard visualizations
## Future Scope
- Real-time KPI streaming
- LSTM based anomaly detection
- Autoencoder based anomaly detection
- Cloud deployment
- Telecom OSS/BSS integration
- Explaianble AI (XAI)
- Automated alert notifications
- Multi-user dashboard with authentication
## Conclusion
The AI Based 5G KPI Anomaly Detection Dashboard demonstrates the practical application of machine learning in telecom network monitoring. By integrating data preprocessing, feature engineering, Isolation Forest anomaly detection, hyperparameter tuning, and an interactive Streamlit dashboard, the project provides a scalable framework for proactive monitoring of 5G network performance.
# Author
*Vibhuti Chaddha*
