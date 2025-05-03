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
    
    filtered_data = Aggre_transaction[(Aggre_transaction["States"] == state) & (Aggre_transaction["Quarter"] == quarter)]
    
    if not filtered_data.empty:
        fig = px.bar(filtered_data, x="Transaction_type", y="Transaction_amount", 
                      title=f"Transaction Dynamics in {state} for Q{quarter}",
                      color="Transaction_type", height=400)
        st.plotly_chart(fig)

def analyze_transaction_market_expansion():
    st.subheader("2. Transaction Analysis for Market Expansion")
    state = st.selectbox("Select State", Aggre_transaction["States"].unique())
    
    filtered_data = Aggre_transaction[Aggre_transaction["States"] == state]
    
    if not filtered_data.empty:
        fig = px.line(filtered_data, x="Quarter", y="Transaction_count", 
                       title=f"Transaction Trends in {state}",
                       color="Transaction_type", height=400)
        st.plotly_chart(fig)

def analyze_insurance_engagement():
    st.subheader("3. Insurance Engagement Analysis")
    state = st.selectbox("Select State", Aggre_insurance["States"].unique())
    
    filtered_data = Aggre_insurance[Aggre_insurance["States"] == state]
    
    if not filtered_data.empty:
        fig = px.bar(filtered_data, x="Transaction_type", y="Transaction_count", 
                      title=f"Insurance Engagement in {state}",
                      color="Transaction_type", height=400)
        st.plotly_chart(fig)

def analyze_transaction_across_states():
    st.subheader("4. Transaction Analysis Across States and Districts")
    filtered_data = Aggre_transaction.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    
    if not filtered_data.empty:
        fig = px.bar(filtered_data, x="States", y="Transaction_amount", 
                      title="Transaction Analysis Across States",
                      color="Transaction_amount", height=400)
        st.plotly_chart(fig)

def analyze_user_registration():
    st.subheader("5. User Registration Analysis")
    year = st.selectbox("Select Year", Aggre_transaction["Years"].unique())
    
    filtered_data = Aggre_transaction[Aggre_transaction["Years"] == year]
    
    if not filtered_data.empty:
        fig = px.bar(filtered_data, x="States", y="Transaction_count", 
                      title=f"User  Registrations in {year}",
                      color="Transaction_count", height=400)
        st.plotly_chart(fig)

def analyze_insurance_transactions():
    st.subheader("6. Insurance Transactions Analysis")
    year = st.selectbox("Select Year", Aggre_insurance["Years"].unique())
    
    filtered_data = Aggre_insurance[Aggre_insurance["Years"] == year]
    
    if not filtered_data.empty:
        fig = px.bar(filtered_data, x="States", y="Transaction_count", 
                      title=f"Insurance Transactions in {year}",
                      color="Transaction_count", height=400)
        st.plotly_chart(fig)

def analyze_user_registration_map():
    st.subheader("7. User Registration Across Indian States (Map)")

    # Cleaning column name if needed
    map_user.columns = [col.strip() for col in map_user.columns]

    # Grouping data for the map
    map_data = map_user.groupby("States")[["RegisteredUser"]].sum().reset_index()

    # India state-level choropleth map
    fig = px.choropleth(
        map_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="States",
        color="RegisteredUser",
        color_continuous_scale="Viridis",
        title="Registered Users Across Indian States",
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
        "5. User Registration Analysis",
        "6. Insurance Transactions Analysis",
        "7. User Registration Across Indian States (Map)"
    ])
    
    if question == "1. Decoding Transaction Dynamics on PhonePe":
        analyze_transaction_dynamics()
    elif question == "2. Transaction Analysis for Market Expansion":
        analyze_transaction_market_expansion()
    elif question == "3. Insurance Engagement Analysis":
        analyze_insurance_engagement()
    elif question == "4. Transaction Analysis Across States and Districts":
        analyze_transaction_across_states()
    elif question == "5. User Registration Analysis":
        analyze_user_registration()
    elif question == "6. Insurance Transactions Analysis":
        analyze_insurance_transactions()
    elif question == "7. User Registration Across Indian States (Map)":
        analyze_user_registration_map()