#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
from PIL import Image


# Establishing the connection
mydb = pymysql.connect(user='root', password='Jeelani19', host='127.0.0.1', database="phonepe")
cursor = mydb.cursor()

# Dataframe Creation
# Aggregated Insurance Data
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()
Aggre_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

# Aggregated Transaction Data
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

# Map Insurance Data
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()
map_insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))

# Map User Data
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()
map_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "District",
                                               "RegisteredUser ", "AppOpens"))

# Top User Data
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()
top_user = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUsers"))


# Business Case Studies Functions
def analyze_transaction_dynamics():
    st.subheader("1. Decoding Transaction Dynamics on PhonePe")
    state = st.selectbox("Select State", Aggre_transaction["States"].unique())
    quarter = st.selectbox("Select Quarter", Aggre_transaction["Quarter"].unique())
    filtered = Aggre_transaction[(Aggre_transaction["States"] == state) & (Aggre_transaction["Quarter"] == quarter)]

    if not filtered.empty:
        # Existing visualizations
        st.plotly_chart(px.bar(filtered, x="Transaction_type", y="Transaction_amount", color="Transaction_type",
                               title=f"Bar_chart for Transaction Amount by Type in {state}, Q{quarter}"))
        st.plotly_chart(px.bar(filtered, x="Transaction_type", y="Transaction_count", color="Transaction_type",
                               title="Bar_chart of Transaction Count by Type"))
        st.plotly_chart(px.pie(filtered, names="Transaction_type", values="Transaction_amount",
                               title="Pie_chart for Share of Transaction Amount by Type"))
        st.plotly_chart(px.scatter(filtered, x="Transaction_count", y="Transaction_amount", color="Transaction_type",
                                   size="Transaction_amount", title="Scatter_plot of Count vs Amount by Transaction Type"))
        top_10_transactions = filtered.nlargest(10, 'Transaction_amount')
        # Visualization for Top 10 Transactions
        st.plotly_chart(px.bar(top_10_transactions, x="Transaction_type", y="Transaction_amount", color="Transaction_type",
                               title="Top 10 Transactions by Amount"))
        # Map Visualization
        map_data = Aggre_transaction.groupby("States")[["Transaction_amount"]].sum().reset_index()
        fig = px.choropleth(
            map_data,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="States",
            color="Transaction_amount",
            color_continuous_scale="Viridis",
            title="Total Transaction Amount Across Indian States",
            hover_name="States",
            hover_data=["Transaction_amount"],
            height=600
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

def analyze_transaction_market_expansion():
    st.subheader("2. Transaction Analysis for Market Expansion")
    state = st.selectbox("Select State", Aggre_transaction["States"].unique())
    filtered = Aggre_transaction[Aggre_transaction["States"] == state]

    if not filtered.empty:
        # Existing visualizations
        st.plotly_chart(px.line(filtered, x="Years", y="Transaction_count", color="Transaction_type",
                                title="Line_chart for Yearly Transaction Count Trend"))
        st.plotly_chart(px.line(filtered, x="Years", y="Transaction_amount", color="Transaction_type",
                                title="Line_chart for Yearly Transaction Amount Trend"))
        st.plotly_chart(px.bar(filtered, x="Quarter", y="Transaction_count", color="Transaction_type",
                               title="Bar_chart for Quarterly Transaction Count"))
        st.plotly_chart(px.scatter(filtered, x="Transaction_count", y="Transaction_amount",
                                   color="Transaction_type", size="Transaction_amount",
                                   title="Scatter_plot of Transaction Volume vs Value"))
        top_10_transactions = filtered.nlargest(10, 'Transaction_count')
        # Visualization for Top 10 Transactions
        st.plotly_chart(px.bar(top_10_transactions, x="Transaction_type", y="Transaction_count", color="Transaction_type",
                               title="Top 10 Transactions by Count"))
        # Map Visualization
        map_data = filtered.groupby("States")[["Transaction_amount"]].sum().reset_index()
        fig = px.choropleth(
            map_data,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="States",
            color="Transaction_amount",
            color_continuous_scale="Viridis",
            title="Transaction Amount by State",
            hover_name="States",
            hover_data=["Transaction_amount"],
            height=600
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

def analyze_insurance_engagement():
    st.subheader("3. Insurance Engagement Analysis")
    year = st.selectbox("Select Year", Aggre_insurance["Years"].unique())
    filtered = Aggre_insurance[Aggre_insurance["Years"] == year]

    if not filtered.empty:
        # Existing visualizations
        st.plotly_chart(px.bar(filtered, x="States", y="Transaction_count", color="Transaction_type",
                               title=f"Bar_chart for Insurance Transactions by State in {year}"))
        st.plotly_chart(px.bar(filtered, x="States", y="Transaction_amount", color="Transaction_type",
                               title="Bar_chart of Insurance Amount by State"))
        st.plotly_chart(px.pie(filtered, names="States", values="Transaction_amount",
                               title="Pie_chart for State-wise Share of Insurance Value"))
        st.plotly_chart(px.scatter(filtered, x="Transaction_count", y="Transaction_amount", color="States",
                                   size="Transaction_amount", title="Scatter_plot of Count vs Amount by State"))
        top_10_insurance = filtered.nlargest(10, 'Transaction_amount')
        # Visualization for Top 10 Insurance Transactions
        st.plotly_chart(px.bar(top_10_insurance, x="States", y="Transaction_amount", color="States",
                               title="Top 10 Insurance Transactions by Amount"))
        # Map Visualization
        map_data = filtered.groupby("States")[["Transaction_amount"]].sum().reset_index()
        fig = px.choropleth(
            map_data,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="States",
            color="Transaction_amount",
            color_continuous_scale="Viridis",
            title="Insurance Amount by State",
            hover_name="States",
            hover_data=["Transaction_amount"],
            height=600
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)

def analyze_transaction_across_states():
    st.subheader("4. Transaction Analysis Across States and Districts")
    grouped = Aggre_transaction.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    if not grouped.empty:
        # Existing visualizations
        st.plotly_chart(px.bar(grouped, x="States", y="Transaction_amount", color="Transaction_amount",
                               title="Bar_chart for Total Transaction Amount by State"))
        st.plotly_chart(px.bar(grouped, x="States", y="Transaction_count", color="Transaction_count",
                               title="Bar_chart of Total Transaction Count by State"))
        st.plotly_chart(px.pie(grouped, names="States", values="Transaction_amount",
                               title="Pie_chart for State-wise Share of Total Transaction Amount"))
        st.plotly_chart(px.scatter(grouped, x="Transaction_count", y="Transaction_amount", color="States",
                                   size="Transaction_amount", title="Scatter_plot of State Transaction Count vs Amount"))   
        top_10_states = grouped.nlargest(10, 'Transaction_amount')
        # Visualization for Top 10 States
        st.plotly_chart(px.bar(top_10_states, x="States", y="Transaction_amount", color="Transaction_amount",
                               title="Top 10 States by Transaction Amount"))
        # Map Visualization
        fig = px.choropleth(
            grouped,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="States",
            color="Transaction_amount",
            color_continuous_scale="Viridis",
            title="Total Transaction Amount Across Indian States",
            hover_name="States",
            hover_data=["Transaction_amount"],
            height=600
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)


def analyze_insurance_transactions():
    st.subheader("5. Insurance Transactions Analysis")
    year = st.selectbox("Select Year", map_insurance["Years"].unique())
    quarter = st.selectbox("Select Quarter", map_insurance["Quarter"].unique())
    filtered = map_insurance[(map_insurance["Years"] == year) & (map_insurance["Quarter"] == quarter)]

    if not filtered.empty:
        # Existing visualizations
        st.plotly_chart(px.bar(filtered, x="States", y="Transaction_count", color="States",
                               title=f"Bar_chart for Insurance Transactions by State in {year} Q{quarter}"))
        st.plotly_chart(px.bar(filtered, x="States", y="Transaction_amount", color="States",
                               title="Bar_chart of Insurance Amount by State"))
        st.plotly_chart(px.pie(filtered, names="States", values="Transaction_amount",
                               title="pie_chart for State-wise Share of Insurance Value"))
        st.plotly_chart(px.scatter(filtered, x="Transaction_count", y="Transaction_amount", color="States",
                                   size="Transaction_amount", title="Scatter_plot of Count vs Amount per State"))
        
        top_10_insurance = filtered.nlargest(10, 'Transaction_amount')
        # Visualization for Top 10 Insurance Transactions
        st.plotly_chart(px.bar(top_10_insurance, x="States", y="Transaction_amount", color="States",
                               title="Top 10 Insurance Transactions by Amount"))

        # Map Visualization
        map_data = filtered.groupby("States")[["Transaction_amount"]].sum().reset_index()
        fig = px.choropleth(
            map_data,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",
            locations="States",
            color="Transaction_amount",
            color_continuous_scale="Viridis",
            title="Insurance Amount by State",
            hover_name="States",
            hover_data=["Transaction_amount"],
            height=600
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)


# Streamlit Part
st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND Business Case Studies")

with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "Business Case Studies"])

if select == "HOME":
    col1, col2 = st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\INDIA\Downloads\phonepe logo.png"), width=600)

elif select == "Business Case Studies":
    question = st.selectbox("Select the Question", [
        "1. Decoding Transaction Dynamics on PhonePe",
        "2. Transaction Analysis for Market Expansion",
        "3. Insurance Engagement Analysis",
        "4. Transaction Analysis Across States and Districts",
        "5. Insurance Transactions Analysis",
    ])
    
    if question == "1. Decoding Transaction Dynamics on PhonePe":
        analyze_transaction_dynamics()
    elif question == "2. Transaction Analysis for Market Expansion":
        analyze_transaction_market_expansion()
    elif question == "3. Insurance Engagement Analysis":
        analyze_insurance_engagement()
    elif question == "4. Transaction Analysis Across States and Districts":
        analyze_transaction_across_states()
    elif question == "5. Insurance Transactions Analysis":
        analyze_insurance_transactions()