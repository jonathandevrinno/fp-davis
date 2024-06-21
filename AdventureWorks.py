# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
from sqlalchemy import create_engine

# Database connection
db = pymysql.connect(host='localhost', user='root', password='', db='adventureworks')
engine = create_engine("mysql+mysqlconnector://root:@localhost/adventureworks")

# Load data
dimtime_df = pd.read_sql("SELECT * FROM dimtime", engine)
dimcustomer_df = pd.read_sql("SELECT * FROM dimcustomer", engine)
dimproduct_df = pd.read_sql("SELECT * FROM dimproduct", engine)
dimproductcategory_df = pd.read_sql("SELECT * FROM dimproductcategory", engine)
dimproductsubcategory_df = pd.read_sql("SELECT * FROM dimproductsubcategory", engine)
factintsales = pd.read_sql("SELECT * FROM factinternetsales", engine)

# Visualization functions
def comparison_plot():
    st.subheader("Perbandingan (Comparison)")
    st.write("Visualisasi ini menunjukkan perbandingan jumlah penjualan tiap tahun menggunakan bar chart.")
    tren_penjualan = factintsales.merge(dimtime_df, left_on='OrderDateKey', right_on='TimeKey')
    tren_penjualan = tren_penjualan.groupby('CalendarYear').agg({'SalesAmount': 'sum'}).reset_index()
    colors = sns.color_palette("hls", len(tren_penjualan))
    plt.figure(figsize=(10, 5))
    sns.barplot(data=tren_penjualan, x='CalendarYear', y='SalesAmount', palette=colors)
    plt.title('Perbandingan Jumlah Penjualan tiap Tahun')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    st.pyplot(plt)

def relationship_plot():
    st.subheader("Hubungan (Relationship)")
    st.write("Visualisasi ini menunjukkan hubungan antara pendapatan tahunan dengan total penjualan menggunakan scatter plot.")
    customer_buy = factintsales.merge(dimcustomer_df, left_on='CustomerKey', right_on='CustomerKey')
    customer_buy = customer_buy.groupby('FirstName').agg({'SalesAmount': 'sum', 'YearlyIncome': 'mean'}).reset_index()
    colors = customer_buy['SalesAmount']
    norm = plt.Normalize(colors.min(), colors.max())
    cmap = plt.cm.coolwarm
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    scatter = plt.scatter(customer_buy['YearlyIncome'], customer_buy['SalesAmount'], c=colors, cmap=cmap, edgecolor='black', alpha=0.7, s=100)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Warna Total Pembelian berdasarkan Jumlah')
    sns.regplot(x='YearlyIncome', y='SalesAmount', data=customer_buy, scatter=False, color='blue', line_kws={"linewidth": 1, "linestyle": "--"})
    plt.title('Hubungan Pendapatan Tahunan dengan Total Penjualan', fontsize=15)
    plt.xlabel('Pendapatan Tahunan', fontsize=12)
    plt.ylabel('Total Penjualan', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(plt)

def composition_plot():
    st.subheader("Komposisi (Composition)")
    st.write("Visualisasi ini menunjukkan komposisi penjualan per subkategori produk menggunakan pie chart.")
    penjualan_product = factintsales.merge(dimproduct_df, left_on='ProductKey', right_on='ProductKey')
    penjualan_subkategori = penjualan_product.merge(dimproductsubcategory_df, left_on='ProductSubcategoryKey', right_on='ProductSubcategoryKey')
    penjualan_subkategori = penjualan_subkategori.groupby('EnglishProductSubcategoryName').agg({'SalesAmount': 'sum'}).reset_index()
    plt.figure(figsize=(10, 7))
    plt.pie(penjualan_subkategori['SalesAmount'], labels=penjualan_subkategori['EnglishProductSubcategoryName'], autopct='%1.1f%%', startangle=140)
    plt.title('Komposisi Penjualan per Subkategori Produk')
    st.pyplot(plt)

def distribution_plot():
    st.subheader("Distribusi (Distribution)")
    st.write("Visualisasi ini menunjukkan distribusi jumlah penjualan menggunakan histogram.")
    penjualan_product = factintsales.merge(dimproduct_df, left_on='ProductKey', right_on='ProductKey')
    plt.figure(figsize=(10, 5))
    sns.histplot(penjualan_product['SalesAmount'], kde=True, bins=30)
    plt.title('Distribusi Jumlah Penjualan')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Frekuensi')
    st.pyplot(plt)

# Streamlit app layout
st.title("Dashboard Visualisasi Data")

option = st.selectbox(
    'Pilih jenis visualisasi:',
    ('Comparison', 'Relationship', 'Composition', 'Distribution')
)

if option == 'Comparison':
    comparison_plot()
elif option == 'Relationship':
    relationship_plot()
elif option == 'Composition':
    composition_plot()
elif option == 'Distribution':
    distribution_plot()
