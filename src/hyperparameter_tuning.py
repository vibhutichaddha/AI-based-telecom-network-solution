import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
df=pd.read_csv("data/processed/telecom_kpi_processed.csv")
features=["RSRP","SINR","Latency","Throughput","Packet_Loss","Connected_Users","Signal_Quality_Score","Network_Load","Network_Health_Index"]
X=df[features]
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
results=[]
estimators=[50,100,200]
contamination_values=[0.01,0.03,0.05,0.10]
for n in estimators:
    for c in contamination_values:
        model=IsolationForest(n_estimators=n,contamination=c,random_state=42)
        predictions=model.fit_predict(X_scaled)
        anomaly_count=(predictions==-1).sum()
        anomaly_percentage=(anomaly_count/len(predictions))*100
        results.append({"Trees":n,"Contamination":c,"Detected_anomalies":anomaly_count,"Anomaly_Percentage":round(anomaly_percentage,2)})
results_df=pd.DataFrame(results)
print(results_df)
results_df.to_csv("reports/hyperparameter_tuning.csv",index=False)
print("\nResults saved successfully")