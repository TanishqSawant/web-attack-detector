import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

sql_count = 0
xss_count = 0
traversal_count = 0

# Dashboard title
st.title("Web Attack Detection Dashboard")

# Simple text
st.write("Real-Time Web Intrusion Detection System")


with open ("alerts.log", "r") as file:
    alerts = file.readlines()

for line in alerts:
    if "SQL Injection" in line:
        sql_count += 1
    elif "XSS Attack" in line:
        xss_count += 1
    elif "Directory Traversal" in line:
        traversal_count += 1


# Attack statistics
st.header("Attack Statistics")

st.write(f"SQL Injection Attacks: {sql_count}")
st.write(f"XSS Attacks: {xss_count}")
st.write(f"Traversal Attacks: {traversal_count}")


ip_counts = {}

for line in alerts:
    ip = line.split("IP: ")[1].split()[0]

    if ip in ip_counts:
        ip_counts[ip] += 1
    else:
        ip_counts[ip] = 1

# Top attacking IPs
st.header("Top Attacking IPs")
for ip, count in ip_counts.items():
    st.write(f"{ip} → {count} attacks")

#Dangerous IPs

most_dangerous_ip = ""
max_attacks = 0

for ip, count in ip_counts.items():
    if count > max_attacks:
        max_attacks = count
        most_dangerous_ip = ip


st.header("Most Dangerous IP")
st.write(f"IP Address: {most_dangerous_ip}")
st.write(f"Attack Count: {max_attacks}")


attack_data = {
    "Attack Type": [
        "SQL Injection",
        "XSS Attack",
        "Directory Traversal"
    ],
    "Count": [
        sql_count,
        xss_count,
        traversal_count
    ]
}


fig = px.pie(
    attack_data,
    names="Attack Type",
    values="Count",
    title="Attack Distribution"
)

st.header("Attack Distribution")
st.plotly_chart(fig)

#Recent Attacks
st.header("Recent Alerts")

with open("alerts.log", "r") as file:

    alerts = file.readlines()

for alert in alerts[-5:]:
    st.write(alert)


#Auto-refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

#Timing of Attacks
attack_times = {}

for line in alerts:
    timestamp = line.split("Time: ")[1].split(" |")[0]

    #Only hour and minute
    time_only = timestamp.split(":")[1] + ":" + timestamp.split(":")[2]

    if time_only in attack_times:
        attack_times[time_only] += 1
    else:
        attack_times[time_only] = 1


st.header("Attack Timeline")

for time,count in attack_times.items():
    st.write(f"{time} → {count} attacks")


#Attack timeline chart
timeline_data = {
    "Time": list(attack_times.keys()),
    "Attacks": list(attack_times.values())
}

fig2 = px.line(
    timeline_data,
    x="Time",
    y="Attacks",
    title="Attack activity over time"
)

st.plotly_chart(fig2)
