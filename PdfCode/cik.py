import pandas as pd
import requests
import os

def get_CIK():
    # Read the Excel file
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Combine the directory path and file name to get the absolute path
    file_path = os.path.join(dir_path, 'List of Tickers.xlsx')

    # Now use pandas to read the file
    xl = pd.ExcelFile(file_path)
    #xl = pd.ExcelFile('List of Tickers.xlsx')
    df = xl.parse(0)  # Replace 'Sheet1' with the name of your sheet
    tickers = df['Ticker'].str.lower().tolist()  # Replace 'B' with the name of your column

    # Create a new DataFrame to hold the results
    result_df = pd.DataFrame(columns=['Ticker', 'CIK'])

    # Fetch the ticker-CIK mapping from the SEC
    response = requests.get('https://www.sec.gov/include/ticker.txt')
    lines = response.text.splitlines()

    # Create a dictionary to map tickers to CIKs
    data = []

    cik_map = {}
    for line in lines:
        ticker, cik = line.split('\t')
        cik_map[ticker] = cik
        data.append({'Ticker': ticker, 'CIK': cik_map[ticker]})

    # Map the tickers in your DataFrame to CIKs


    # Concatenate the data to the result DataFrame
    result_df = pd.concat([result_df, pd.DataFrame(data)])
    result_df['CIK'] = result_df['CIK'].astype(
        str).str.zfill(10)
    return result_df

def get_CIK_num():
    df = get_CIK()
    ticker_cik_dict = df.set_index('Ticker')['CIK'].to_dict()
    return ticker_cik_dict


# Print the results
get_CIK().to_excel("cik.xlsx", index=False)