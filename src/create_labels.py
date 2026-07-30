import pandas as pd
df = pd.read_csv("data/processed/telecom_kpi_with_anomalies.csv")
def create_label(row):
    if (row["RSRP"] < -105 or row["SINR"] < 10 or row["Latency"] > 100 or row["Packet_Loss"] > 5):
        return "Anomaly"
    return "Normal"

df["Actual_Label"] = df.apply(create_label, axis=1)
df.to_csv("data/processed/telecom_kpi_with_anomalies.csv",index=False)
print("Actual_Label column created successfully.")