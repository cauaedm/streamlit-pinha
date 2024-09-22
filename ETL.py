import pandas as pd
from datetime import datetime
import numpy as np
import requests
from datetime import datetime, timedelta
from io import BytesIO
import pdfplumber
from datetime import datetime, timedelta


def get_data(pdf_url):
    data = pdf_url.split('/')[7].split('.')[0] + '-' + pdf_url.split('/')[6] + '-' + pdf_url.split('/')[5]
    return datetime.strptime(data, "%d-%m-%Y")


def new_pdf(date):
    if date.day > 9:
        if date.month > 9:
            return f'http://www.sde.ba.gov.br/wp-content/uploads/{date.year}/{date.month}/{date.day}.{date.month}.{date.year}.pdf'
        return f'http://www.sde.ba.gov.br/wp-content/uploads/{date.year}/0{date.month}/{date.day}.0{date.month}.{date.year}.pdf'
    
    if date.month > 9:
        return f'http://www.sde.ba.gov.br/wp-content/uploads/{date.year}/{date.month}/0{date.day}.{date.month}.{date.year}.pdf'
    
    return f'http://www.sde.ba.gov.br/wp-content/uploads/{date.year}/0{date.month}/0{date.day}.0{date.month}.{date.year}.pdf'

def get_pdf(pdf_url, verboose=True):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Verificar se a requisição foi bem-sucedida
        pdf_file = BytesIO(response.content)
        
        texto = ''
    
        with pdfplumber.open(pdf_file) as pdf:

            for page_number, page in enumerate(pdf.pages):
                texto_novo = page.extract_text()
                texto = texto + texto_novo
                
        return texto
    except requests.exceptions.Timeout:
        if verboose:
            print('A requisição demorou muito para responder.')
    except requests.exceptions.RequestException as e:
        if verboose:
            print(f'Erro ao fazer a requisição: {e}')
    except Exception as e:
        if verboose:
            print(f'Outro erro ocorreu: {e}')


def get_series(produto, data_final, verboose=True):
    
    erro = 0
    
    series = {
        'Produto': [],
        'Data': [],
        'Preco': []
    }
    data_atual = datetime.now()

    while data_atual > data_final:
        if verboose:
            print(data_atual.strftime("%Y-%m-%d"))
        
        data_formatada = data_atual.strftime("%Y-%m-%d")
        
        # Supondo que new_pdf e get_pdf são funções definidas em outro lugar
        texto = get_pdf(new_pdf(data_atual), verboose)

        # Verificar se texto não é None
        if texto is None or '404 Client Error' in texto:
            erro += 1
            
            if erro == 100:
                break
            
            data_atual -= timedelta(days=1)
            continue

        # Supondo que linhas é uma lista de strings obtida do texto
        linhas = texto.split('\n')

        for linha in linhas:
            if produto in linha:
                # Extraindo a data e o preço da linha
                preco_str = linha.split()[4]  # Ajuste conforme o formato real da linha
                series['Produto'].append(linha.split(' ')[0])
                series['Data'].append(data_formatada)
                series['Preco'].append(preco_str)

        data_atual -= timedelta(days=1)
        
        erro = 0

    return series

def dict_to_dataframe(data_dict):
    df = pd.DataFrame(data_dict)
    
    return df

def uptade_data(old_path=None):
    old_data = pd.read_csv('data.csv')
    most_recent_date = old_data['Data'][0]

    data_final = datetime.strptime(most_recent_date, "%Y-%m-%d")

    # Chamar a função (df deve ser um DataFrame definido em outro lugar)
    resultado = get_series('PINHA', data_final)

    new_df = pd.DataFrame.from_dict(resultado)

    new_df['Preco'] = new_df['Preco'].str.replace(',', '.')

    # Converta a coluna para numérico
    new_df['Preco'] = pd.to_numeric(new_df['Preco'])
    
    new_df = pd.concat([new_df, old_data])
    new_df.to_csv('data.csv', index=False)


if __name__ == "__main__":
    uptade_data()
    pass