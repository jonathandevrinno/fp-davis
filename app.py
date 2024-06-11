import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Set the page icon
st.set_page_config(page_title="FINAL PROJECT VISUALISASI DATA", 
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Set the page title
st.title("Final Project Visualisasi Data")

# Owner Name
st.header("Ownership:")
st.markdown("This task is created by: \n[Jonathan Devrinno](https://www.linkedin.com/in/jonathandevrinno/) (21082010204)")

# Sidebar menu
option = st.sidebar.selectbox("Select a feature", ["AdventureWorks", "IMDb Scrapping"])

if option == "📄 AdventureWorks":
  # Membuat koneksi ke database
    db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="aw"
)
  
elif option == "📽️ IMDb Scrapping":
