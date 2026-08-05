import streamlit as st
import logging 
import pandas as pd
import plotly.express as px
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",)
logger = logging.getLogger(__name__)
st.set_page_config(page_title="5G KPI Anomaly Detection Dasboard",layout="wide")
st.title("AI-Based 5G KPI Anomaly Detection Dashboard")
st.markdown("Monitor telecom KPIs and detect anomalies using and Isolation Forest model")
@st.cache_data
def load_data():
    try:
        dataframe=pd.read_csv("data/processed/telecom_kpi_with_anomalies.csv")
        dataframe["Timestamp"]=pd.to_datetime(dataframe["Timestamp"])
        logger.info("Dataset loaded successfully")
        return dataframe
    except FileNotFoundError:
        st.error("Dataset not found")
        logger.error("Dataset not found")
        st.stop()
    except Exception as error:
        st.error(f"Error loading dataset: {error}")
        logger.exception(error)
        st.stop()
df=load_data()
st.sidebar.header("Filters")
selected_cell=st.sidebar.selectbox("Select Cell ID",["All"]+sorted(df["Cell_ID"].unique().tolist()))
if selected_cell!="All":
    df=df[df["Cell_ID"]==selected_cell]
st.header("Network Summary")
col1,col2,col3,col4=st.columns(4)
col1.metric("Total Records",len(df))
col2.metric("Normal",(df["Anomaly"]=="Normal").sum())
col3.metric("Anomalies",(df["Anomaly"]=="Anomaly").sum())
col4.metric("Average Throughput",f"{df['Throughput'].mean():.2f}Mbps")
st.header("Throughput Trend")
fig=px.line(df,x="Timestamp",y="Throughput",title="Throughput over time")
st.plotly_chart(fig,use_container_width=True)
st.header("Latency Trend")
fig=px.line(df,x="Timestamp",y="Latency",title="Latency over time")
st.plotly_chart(fig,use_container_width=True)
st.header("SINR Distribution")
fig=px.histogram(df,x="SINR",nbins=25,title="SINR Distribution")
st.plotly_chart(fig,use_container_width=True)
st.header("RSRP vs Throughput")
fig=px.scatter(df,x="RSRP",y="Throughput",color="Anomaly",title="RSRP vs Throughput")
st.plotly_chart(fig,use_container_width=True)
st.header("Anomaly Distribution")
fig=px.pie(df,names="Anomaly",title="Normal vs Anomaly")
st.plotly_chart(fig,use_container_width=True)
st.header("Detected Anomalies")
st.dataframe(df[df["Anomaly"]=="Anomaly"],use_container_width=True,)
st.download_button(label="Download Results",data=df.to_csv(index=False),file_name="telecom_kpi_with_anomalies.csv",mime="text/csv")