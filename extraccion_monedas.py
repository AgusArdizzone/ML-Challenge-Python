import requests
import pandas as pd
import os

url = "https://economia.awesomeapi.com.br/json/last/"
currency = "USD-BRL,EUR-BRL,BTC-BRL"

def get_currency_data(url,currency):

    try:
        # Get data from the API
        currency_data = requests.get(url + currency)
        # Check if the response is valid
        if currency_data.status_code != 200:
            raise Exception("Status code not 200")
        
        # If response is OK, return the json file
        return currency_data.json()

    except Exception as e:
        # Print the error message in console and return None
        print(f"Error fetching currency data: {e}")
        return None


def transform_currency_data(data):

    currency_df = pd.DataFrame(data).T
    currency_df = currency_df[['code', 'codein', 'bid', 'ask', 'timestamp']]
    currency_df = currency_df.rename(columns={
        'code': 'moneda_base',
        'codein': 'moneda_destino',
        'bid': 'valor_compra',
        'ask': 'valor_venta',
        'timestamp': 'data_hora'
    })
    
    # Transform the 'data_hora' column from UNIX timestamp to datetime
    currency_df['data_hora'] = pd.to_datetime(pd.to_numeric(currency_df['data_hora']), unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    return currency_df

def merge_currency_data(new_data, existing_data):
    # Merge the new data with the existing data
    merged_data = pd.concat([existing_data, new_data], ignore_index=True)
    
    # Drop duplicates based on 'moneda_base', 'moneda_destino' and 'data_hora'
    merged_data = merged_data.drop_duplicates(subset=['moneda_base', 'moneda_destino', 'data_hora'], keep='last')
    
    return merged_data

def save_currency_data(currency_df):
    
    # Create a directory (if it not exists) to save the data.
    if not os.path.exists('data'):
        os.makedirs('data')

    # Check if file exists, if it does, merge the new data with the existing data
    if os.path.exists('data/datos_monedas.csv'):
        existing_data = pd.read_csv('data/datos_monedas.csv')
        merged_data = merge_currency_data(currency_df, existing_data)

    # Save the data in a csv file
    merged_data.to_csv('./data/datos_monedas.csv', index=False)
    print("Data saved to data/datos_monedas.csv")
    
print("Starting to fetch currency data...")
currency_data = get_currency_data(url, currency)

# If the return data of get_currency_data is not None, proceed to transform and save the currency data
if currency_data:
    currency_df = transform_currency_data(currency_data)
    save_currency_data(currency_df)
    print("Data transformation and saving completed.")