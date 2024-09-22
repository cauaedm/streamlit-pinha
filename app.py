# import the streamlit library
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ETL
import plotly.express as px

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
st.metric(label=f"Última divulgação {df['Data'][0].split('-')[2]}/{df['Data'][0].split('-')[1]}/{df['Data'][0].split('-')[0]}", value=f"R${latest_price:.2f}", delta=f"R${price_change:.2f}")

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

col1, col2 = st.columns(2)

# Colocar as métricas dentro das colunas
with col1:
    st.metric(label="Média do último ano:", value=f"{np.mean(np.array(df['Preco'][:12])):.2f}", delta=f"{(np.mean(np.array(df['Preco'][:12]) - np.array(df['Preco'][12:24]))):.2f}")

with col2:
    st.metric(label="ada", value=10)

    
df["month"] = df['Data'].str.split('-').str[1]

# Agrupar pelo mês e calcular a média dos preços
mean_prices = df['Preco'].groupby(df['month']).mean().reset_index()
mean_prices.columns = ['month', 'mean_price']  # Renomear colunas

# Criar o gráfico de barras com Plotly
fig = px.bar(mean_prices, x='month', y='mean_price', 
              title='Média de Preços por Mês', 
              labels={'month': 'Mês', 'mean_price': 'Média de Preços'},
              color='mean_price')

# Configurar o layout do gráfico
fig.update_layout(xaxis_title='Mês', yaxis_title='Média de Preços')
fig.update_yaxes(type='log')

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)