import streamlit as st

# Set the page icon
st.set_page_config(page_title="FINAL PROJECT VISUALISASI DATA", 
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Set the page title
st.title("Final Project Visualisasi Data")
# Owner Name
st.header("Ownership:")
st.markdown("This task is created by: \n[Jonathan Devrinno](https://www.linkedin.com/in/jonathandevrinno/) \nNPM:21082010204.")

# Sidebar menu
option = st.sidebar.selectbox("Select a feature", ["AdventureWorks", "IMDb Scrapping"])

if option == "AdventureWorks":
  
elif option == "IMDb Scrapping":
