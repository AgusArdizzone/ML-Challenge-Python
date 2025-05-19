import requests
import pandas as pd
import os

url = "https://economia.awesomeapi.com.br/json/last/"
currency = "USD-BRL,EUR-BRL,BTC-BRL"

def get_currency_data(url,currency):
    """
    Function to get data from the API. Checks if the response is OK
    and returns the json file. If its not OK, it raises an exception.
    
    Args:
        url (string): the url of the API we will use
        currency (string): the info of the currencies to get from the API

    Raises:
        Exception: When the status code is not 200, raises and exception and prints the error.

    Returns:
        dict: Returns the json file in a dict format. If a exception is raised, returns None.
    """
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


def transform_currency_json_to_df(currency_json):
    """
    Transform the data from a JSON to a DataFrame.
    it will pivot the data to get the info of the   

    Args:
        currency_json (dict): a dict that contains the data 
        of the currencies exchange rates.

    Returns:
        Dataframe: Returns a DataFrame with the following data:
        - moneda_base: The base currency
        - moneda_destino: The destination currency
        - valor_compra: The buy value
        - valor_venta: The sell value
        - data_hora: The date and time of the exchange rate
    """

    currency_df = pd.DataFrame(currency_json).T
    
    #Filter the columns we need
    currency_df = currency_df[['code', 'codein', 'bid', 'ask', 'timestamp']]
    
    # Rename the columns to have the values better represented
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
    """
    Receives two dataframes, one with the data fetched in this script 
    and other with already existing data.
    If there is any duplicate data, it will drop the duplicates.

    Args:
        new_data (DataFrame): Contains the data fetched in this script
        existing_data (DataFrame): Contains data already existing.

    Returns:
        DataFrame: it will return a DataFrame with the merged data.
    """
    # Merge the new data with the existing data
    merged_data = pd.concat([existing_data, new_data], ignore_index=True)
    
    # Drop duplicates based on 'moneda_base', 'moneda_destino' and 'data_hora'
    merged_data = merged_data.drop_duplicates()
    
    return merged_data

def save_currency_data(currency_df):
    """Save the currency data to a CSV file.
       It will save the csv in a "data" folder (and create it if it does not exist).
       If a csv file already exists, it will merge the new data with the existing one.
    Args:
        currency_df (DataFrame): receives the DataFrame with the data to save in the csv.
    """
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


# Main script
print("Starting to fetch currency data...")
currency_data = get_currency_data(url, currency)

# If the return data of get_currency_data is not None, proceed to transform and save the currency data
if currency_data:
    currency_df = transform_currency_json_to_df(currency_data)
    save_currency_data(currency_df)
    print("Data transformation and saving completed.")