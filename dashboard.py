import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
cust_orders = pd.read_csv('merged_cust_orders.csv')
pay_rev = pd.read_csv('merged_pay_rev.csv')

# Merge data based on 'order_id'
merged_data = pd.merge(cust_orders, pay_rev, on='order_id')

# Title of the Dashboard
st.title("Dashboard Analisis Pembelian dan Ulasan Pelanggan")

# Sidebar for filters
st.sidebar.header("Filter Data")
selected_state = st.sidebar.selectbox("Pilih Negara Bagian", merged_data['customer_state'].unique())
selected_payment_type = st.sidebar.multiselect("Pilih Metode Pembayaran", merged_data['payment_type'].unique(), default=merged_data['payment_type'].unique())

# Filter data based on selections
filtered_data = merged_data[(merged_data['customer_state'] == selected_state) & 
                            (merged_data['payment_type'].isin(selected_payment_type))]

# Display data summary
st.subheader("Ringkasan Data")
if not filtered_data.empty:
    st.write(filtered_data.describe())
else:
    st.write("Tidak ada data yang sesuai dengan filter ini.")

# 1. Visualisasi korelasi antara customer state dan purchase time (Pertanyaan Bisnis 1)
st.subheader("Korelasi antara Customer State dan Waktu Pembelian")
if not filtered_data.empty:
    state_time_corr = pd.crosstab(filtered_data['customer_state'], filtered_data['purchase_hour'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(state_time_corr, cmap='coolwarm', linewidths=0.5, linecolor='black', ax=ax)
    ax.set_title("Heatmap Customer State vs Purchase Time")
    st.pyplot(fig)
else:
    st.write("Tidak ada data yang dapat ditampilkan untuk grafik ini.")

# 2. Visualisasi korelasi antara payment type dan review score (Pertanyaan Bisnis 2)
st.subheader("Korelasi antara Payment Type dan Skor Ulasan")
if not filtered_data.empty:
    payment_review_corr = pd.crosstab(filtered_data['payment_type'], filtered_data['review_score'])
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(payment_review_corr, cmap='Blues', linewidths=0.5, linecolor='black', annot=True, ax=ax2)
    ax2.set_title("Heatmap Payment Type vs Review Score")
    st.pyplot(fig2)
else:
    st.write("Tidak ada data yang dapat ditampilkan untuk grafik ini.")