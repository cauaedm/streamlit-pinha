# import the streamlit library
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ETL


# read the data
df = pd.read_csv('data.csv')
data = np.array(df['Preco'])

# Streamlit app title
st.title('Pinha Time Series Scraper')

if st.button("Update data"):
    ETL.uptade_data()

    df = pd.read_csv('data.csv')


# Exibir o último preço de forma destacada
latest_price = df['Preco'][0]
previous_price = df['Preco'][1]  # Supondo que o segundo valor é o anterior

# Calcular a variação
price_change = latest_price - previous_price

# Exibir o valor do último preço como métrica
st.metric(label="Último Preço", value=f"R${latest_price:.2f}", delta=f"R${price_change:.2f}")

# Create Plotly figure
fig = go.Figure()

# Add time series data
fig.add_trace(go.Scatter(x=df['Data'], y=df['Preco'], mode='lines', name='Value'))

# Customize layout
fig.update_layout(title='Time Series Plot',
                  xaxis_title='Date',
                  yaxis_title='Value')

# Display the plot in Streamlit
st.plotly_chart(fig)
