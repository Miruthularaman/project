import streamlit as st
import pandas as pd
import math
import numpy as np
import plotly.express as px
from numerize.numerize import numerize
from st_aggrid import AgGrid
import toml
config = toml.load('.streamlit/config.toml')
st.set_page_config(
page_title='Dashboard',
layout = "wide",
initial_sidebar_state = "expanded"
)
st.markdown(
f"""
<style>
.reportview-container {{
background-color: #87CEFg;
}}
</style>
""",
unsafe_allow_html=True
)
## Preprocessing the data
def get_data():
df = pd.read_csv("heartinfo.csv")
## Extracting the date feature from date
df["Date"] = pd.to_datetime(df["Date"]).dt.date
df["Time"] = pd.to_datetime(df["Time"], format = "%H:%M:%S").dt.time
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df["Month"] = pd.to_datetime(df["Date"]).dt.month
df["Month_Name"] = pd.to_datetime(df["Date"]).dt.month_name()
df["Day"] = pd.to_datetime(df["Date"]).dt.day
df["Day_Name"] = pd.to_datetime(df["Date"]).dt.day_name()
df["Hours"] = pd.to_datetime(df["Time"], format = "%H:%M:%S").dt.hour
df["Minutes"] = pd.to_datetime(df["Time"], format = "%H:%M:%S").dt.minute
df["Second"] = pd.to_datetime(df["Time"], format = "%H:%M:%S").dt.second
return df
data = get_data()
## Filters
with st.sidebar:
yearfilter = st.multiselect(
label = "select the year",
options = data["Year"].unique(),
default = data["Year"].unique()
)
monthfilter = st.multiselect(
label = "select the month",
options = data["Month_Name"].unique(),
default = data["Month_Name"].unique()
)
dayfilter = st.multiselect(
label = "select the day",
options = data["Day"].unique(),
default = data["Day"].unique()
)
datafilter = data.query(
'Year == @yearfilter & Month_Name == @monthfilter & Day == @dayfilter'
)
header_left,header_mid,header_right = st.columns([1,3,1],gap = "large")
with header_mid:
title_alignment = """<style>
#the-title {
text-align: center
}
</style>"""
st.markdown(" # Health Dashboard")
st.markdown(title_alignment, unsafe_allow_html=True)
##st.dataframe(datafilter[["Bpm","SPO2","Temperature"]])
## Top Kpi's
average_bpm = int(datafilter["Bpm"].mean())
average_saturation = int(datafilter["SPO2"].mean())
average_temperature = float(datafilter["Temperature"].mean())
max_bpm = int(datafilter["Bpm"].max())
bpmkpi,saturationkpi,temperaturekpi,maxbpmkpi = st.columns(4, gap = "large")
with bpmkpi:
st.image("Templates/heart_rate.png",use_column_width = "auto")
st.metric(label = "Avg Bpm", value = numerize(average_bpm))
with saturationkpi:
st.image("Templates/blood_saturation.png",use_column_width = "auto")
st.metric(label = "Avg SPO2", value = numerize(average_saturation))
with temperaturekpi:
st.image("Templates/temperature.png",use_column_width = "auto")
st.metric(label = "Avg Temperature", value = numerize(average_temperature))
with maxbpmkpi:
st.image("Templates/heart_rate.png",use_column_width = "auto")
st.metric(label = "Max Bpm", value = numerize(max_bpm))
## Charts (1,2)
## 1. bpm by days,hours
## 2. bpm by days,hours,minutes
Q1,Q2 = st.columns(2)
with Q1:
gpdata = datafilter.groupby(by = ["Hours"]).mean()[["Bpm"]].reset_index()
gpdata["Bpm"] = gpdata["Bpm"].astype(int)
bpm_by_hours_fig = px.line(gpdata, x = "Hours", y = "Bpm", title = "Heart Rate By
Hours")
bpm_by_hours_fig.update_layout(xaxis = (dict(showgrid = False)),
yaxis = (dict(showgrid = False)),
title = {'x' : 0.5}
)
st.plotly_chart(bpm_by_hours_fig,use_container_width = True)
with Q2:
color = ["#ED4736"]
gpdata = datafilter.groupby(by = ["Minutes"]).mean()[["Bpm"]].reset_index()
gpdata["Bpm"] = gpdata["Bpm"].astype(int)
bpm_by_minutes_fig = px.line(gpdata, x = "Minutes", y = "Bpm",color_discrete_sequence
= color, title = "Heart Rate By Minutes")
bpm_by_minutes_fig.update_layout(xaxis = (dict(showgrid = False)),
yaxis = (dict(showgrid = False)),
title = {'x' : 0.5}
)
st.plotly_chart(bpm_by_minutes_fig,use_container_width = True)
Q3,Q4 = st.columns(2)
gspdata = datafilter.groupby(by = ["Hours"]).mean()[["SPO2"]].reset_index()
gspdata["SPO2"] = gspdata["SPO2"].astype(int)
gspmdata = datafilter.groupby(by = ["Minutes"]).mean()[["SPO2"]].reset_index()
gspmdata["SPO2"] = gspmdata["SPO2"].astype(int)
with Q3:
def set_status(df):
if(df["SPO2"] < 95):
return "low"
else:
return "normal"
gspdata["Status"] = gspdata.apply(set_status, axis=1)
bpm_by_hours_fig = px.line(gspdata, x = "Hours", y = "SPO2",color="Status", title =
"blood saturation By Hours")
bpm_by_hours_fig.update_layout(xaxis = (dict(showgrid = False)),
yaxis = (dict(showgrid = False)),
title = {'x' : 0.5}
)
st.plotly_chart(bpm_by_hours_fig,use_container_width = True)
with Q4:
color = ["#0CD312","#ED4736"]
def set_status(df):
if(df["SPO2"] < 95):
return "low"
else:
return "normal"
gspmdata["Status"] = gspmdata.apply(set_status, axis=1)
bpm_by_hours_fig = px.line(gspmdata, x = "Minutes", y =
"SPO2",color="Status",color_discrete_sequence = color, title = "blood saturation By
Minutes")
bpm_by_hours_fig.update_layout(xaxis = (dict(showgrid = False)),
yaxis = (dict(showgrid = False)),
title = {'x' : 0.5}
)
st.plotly_chart(bpm_by_hours_fig,use_container_width = True)
Q5,Q6 = st.columns(2)
gspdata1 = datafilter.groupby(by = ["Day"]).mean()[["SPO2","Bpm"]].reset_index()
gspdata1["SPO2"] = gspdata["SPO2"].astype(int)
with Q5:
color = ["#0CD312","#ED4736"]
def set_status(df):
if(df["Bpm"] > 100):
return "Stress"
else:
return "Normal"
gspdata1["Status"] = gspdata1.apply(set_status, axis=1)
gspdata2 = gspdata1.groupby(by = ["Status"]).count().reset_index()
fig_stress = px.pie(gspdata2,
names='Status',
values = 'Day',
color = "Status",
color_discrete_sequence = color,
hole = 0.5,
title='<b>Overall Mental Stability</b>')
fig_stress.update_layout(title = {'x' : 0.5},
plot_bgcolor = "rgba(0,0,0,0)",
)
st.plotly_chart(fig_stress,use_container_width=True)
with Q6:
hrvdata = datafilter.groupby('Day').agg(Bpm_variation=('Bpm', 'var')).reset_index()
hrvdata["Bpm_variation"] = hrvdata['Bpm_variation'].round(decimals = 0)
color = ["#ED4736"]
hrv_fig = px.bar(hrvdata,
x='Day',
y='Bpm_variation',
color_discrete_sequence = color,
title='<b>Heart Rate Variability</b>')
hrv_fig.update_layout(title = {'x' : 0.5},
plot_bgcolor = "rgba(0,0,0,0)",
xaxis =(dict(showgrid = False)),
yaxis =(dict(showgrid = False)))
st.plotly_chart(hrv_fig,use_container_width=True)
# Primary accent color for interactive elements.
primaryColor = "#05445E"
# Background color for the main content area.
backgroundColor = "#D4F1F4"
# Background color used for the sidebar and most interactive widgets.
#secondaryBackgroundColor = "#DCDEE6"
secondaryBackgroundColor = "#189AB4"
# Color used for almost all text.
#textColor = "#000000"
# Font family for all text in the app, except code blocks. One of "sans serif", "serif", or
"monospace".
# Default: "sans serif"
font = "sans serif"
#include <Wire.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include "MAX30100_PulseOximeter.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN D4
#define DHTTYPE DHT11
DHT_Unified dht(DHTPIN, DHTTYPE);
MAX30100_PulseOximeter pox;
const char *ssid = "your_wifi_ssid";
const char *password = "your_wifi_password";
const char *ntpServerName = "pool.ntp.org";
const long gmtOffset_sec = 3600; // Adjust this according to your time zone
const int daylightOffset_sec = 3600; // Adjust this according to your time zone
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, ntpServerName, gmtOffset_sec, daylightOffset_sec);
void setup() {
Serial.begin(9600);
// Connect to Wi-Fi
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
Serial.println("Connecting to WiFi...");
}
Serial.println("Connected to WiFi");
// Initialize sensors
dht.begin();
pox.begin();
pox.setup();
// Initialize NTPClient
timeClient.begin();
timeClient.update();
}
void loop() {
// Update time
timeClient.update();
// Read temperature and humidity
sensors_event_t event;
dht.temperature().getEvent(&event);
if (isnan(event.temperature)) {
Serial.println("Error reading temperature from DHT!");
}
else {
Serial.print("Temperature: ");
Serial.print(event.temperature);
Serial.println(" *C");
}
dht.humidity().getEvent(&event);
if (isnan(event.relative_humidity)) {
Serial.println("Error reading humidity from DHT!");
delay(1000);
Serial.println("Connecting to WiFi...");
}
Serial.println("Connected to WiFi");
// Initialize sensors
dht.begin();
pox.begin();
pox.setup();
// Initialize NTPClient
timeClient.begin();
timeClient.update();
}
void loop() {
// Update time
timeClient.update();
// Read temperature and humidity
sensors_event_t event;
dht.temperature().getEvent(&event);
if (isnan(event.temperature)) {
Serial.println("Error reading temperature from DHT!");
}
else {
Serial.print("Temperature: ");
Serial.print(event.temperature);
Serial.println(" *C");
}
dht.humidity().getEvent(&event);
if (isnan(event.relative_humidity)) {
Serial.println("Error reading humidity from DHT!");