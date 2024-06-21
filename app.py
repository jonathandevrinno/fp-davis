import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#  Import pymysql dan menghandle error
try:
    import pymysql
    from sqlalchemy import create_engine
except ImportError:
    st.warning("pymysql or sqlalchemy is not installed. Please install them to use AdventureWorks visualization.")

# Icon Halaman
st.set_page_config(page_title="FINAL PROJECT VISUALISASI DATA", 
                   page_icon=":bar_chart:",
                   initial_sidebar_state="expanded")

# Judul Halaman
st.title("Final Project Visualisasi Data")

# Watermark
st.header("Ownership:")
st.markdown("This task is created by: \n[Jonathan Devrinno](https://www.linkedin.com/in/jonathandevrinno/) (21082010204)")

# Sidebar menu
option = st.sidebar.selectbox("Select a feature", ["AdventureWorks", "IMDb Scrapping"])

# Visualisasi AdventureWorks
if option == "AdventureWorks":
    try:
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

        # Layout AdventureWorks
        st.title("Dashboard Visualisasi Data AdventureWorks")

        visualization_type = st.selectbox(
            'Pilih jenis visualisasi:',
            ('Comparison', 'Relationship', 'Composition', 'Distribution')
        )

        if visualization_type == 'Comparison':
            comparison_plot()
        elif visualization_type == 'Relationship':
            relationship_plot()
        elif visualization_type == 'Composition':
            composition_plot()
        elif visualization_type == 'Distribution':
            distribution_plot()

    except Exception as e:
        st.error(f"Error: {e}")

# Visualisasi Scrapping IMDb
elif option == "IMDb Scrapping":
    # Fungsi untuk mengubah format menjadi miliar
    def billions(x, pos):
        return '%1.1fB' % (x * 1e-9)

    # Fungsi untuk format autopct
    def autopct_format(values):
        def my_format(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}B\n({p:.1f}%)'.format(p=pct,v=val)
        return my_format

    # Judul
    st.markdown("<h1 style='text-align: center; color: #F4C2C2;'>Tugas Data Visualisasi</h1>", unsafe_allow_html=True)

    # Sumber data
    st.markdown("[Indonesia Box Office Mojo](https://www.boxofficemojo.com/weekend/by-year/2024/?area=ID) - Data diambil dari Indonesia Box Office Mojo")

    # Memuat data dari file CSV
    df = pd.read_csv('film_data_2024.csv')

    # Cleaning kolom 'Pendapatan'
    df['Pendapatan'] = df['Pendapatan'].replace('-', 0)

    # Konversu kolom 'Pendapatan' ke tipe data float
    df['Pendapatan'] = df['Pendapatan'].replace('[\$,]', '', regex=True).astype(float)

    # Menghitung total pendapatan per distributor
    revenue_by_distributor = df.groupby('Distributor')['Pendapatan'].sum().sort_values(ascending=False)

    # Fungsi untuk menampilkan deskripsi film dari distributor yang dipilih
    def display_movie_description(selected_distributor):
        selected_movies = df[df['Distributor'] == selected_distributor]
        if not selected_movies.empty:
            st.write(selected_movies)
        else:
            st.write("Tidak ada film yang didistribusikan oleh", selected_distributor)

    # Dropdown menu untuk memilih distributor
    dropdown_options = list(revenue_by_distributor.index)
    dropdown_options.sort() 
    dropdown_options.insert(0, 'Pilih Distributor')

    # Dropdown menu di Streamlit
    selected_distributor = st.selectbox('Pilih Distributor:', dropdown_options)
    if selected_distributor != 'Pilih Distributor':
        display_movie_description(selected_distributor)

    # Menampilkan pie chart menggunakan matplotlib di Streamlit
    st.write('## Persentase Pendapatan per Distributor pada Tahun 2024')
    colors = ['#FFC0CB', '#FF69B4', '#DDA0DD', '#9370DB', '#ADD8E6', '#87CEFA', '#B0C4DE', '#00BFFF', '#1E90FF', '#6495ED']
    plt.figure(figsize=(10, 6))
    plt.pie(revenue_by_distributor, labels=revenue_by_distributor.index, autopct=autopct_format(revenue_by_distributor), startangle=140, colors=colors)
    plt.axis('equal')
    st.pyplot(plt)

    # Bar Chart: Top 10 Distributors dari Total Revenue
    st.write('## Top 10 Distributors dari Total Revenue')
    top_10_distributors = revenue_by_distributor.head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_distributors.values, y=top_10_distributors.index, palette="Blues_d")
    plt.title('Top 10 Distributors by Total Revenue')
    plt.xlabel('Total Revenue')
    plt.ylabel('Distributor')
    st.pyplot(plt)

    # Line Chart: Tren pendapatan secara waktu menurut distributor
    st.write('## Tren pendapatan secara waktu menurut distributor')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d-%m-%Y')
    distributors_to_plot = st.multiselect('Pilih Distributor untuk Melihat Tren Pendapatan:', options=revenue_by_distributor.index.tolist(), default=revenue_by_distributor.index.tolist()[:3])
    if distributors_to_plot:
        df_filtered = df[df['Distributor'].isin(distributors_to_plot)]
        plt.figure(figsize=(12, 6))
        for distributor in distributors_to_plot:
            df_dist = df_filtered[df_filtered['Distributor'] == distributor]
            df_dist = df_dist.groupby('Tanggal')['Pendapatan'].sum().reset_index()
            plt.plot(df_dist['Tanggal'], df_dist['Pendapatan'], label=distributor)
        plt.title('Revenue Trends Over Time')
        plt.xlabel('Tanggal')
        plt.ylabel('Pendapatan')
        plt.legend()
        st.pyplot(plt)
