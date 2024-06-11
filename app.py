import streamlit as st

# Set the page icon
st.set_page_config(page_title="FINAL PROJECT VISUALISASI DATA", 
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Set the page title
st.title("Final Project Visualisasi Data")

# Sidebar menu
option = st.sidebar.selectbox("Select a feature", ["AdventureWorks", "IMDb Scrapping"])

if option == "AdventureWorks":
    # Owner Name
    st.header("Ownership:")
    st.markdown("This task is created by:\n[Jonathan Devrinno](https://www.linkedin.com/in/jonathandevrinno/)\nNPM:21082010204.")
  
  # Data Visualisation page
    st.header("Data Visualisation")
    st.text("")
  
elif option == "IMDb Scrapping":
    # Owner Name
    st.header("Ownership:")
    st.markdown("This task is created by [Jonathan Devrinno](https://www.linkedin.com/in/jonathandevrinno/) \n(21082010204).")
