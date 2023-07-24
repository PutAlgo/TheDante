import requests
import json
import cik
cik_dict = cik.get_CIK_num()
headers = {
    'User-Agent': "marciuolo7@gmail.com"
}

base_url = 'https://www.sec.gov/Archives/edgar/data'

def get_url(cik, form, range):
    num = cik_dict[cik]
    print(num)
    print()
    resp = requests.get(f'https://data.sec.gov/submissions/CIK{num}.json', headers=headers)
    #print(resp.content)
    #print()
    # Convert the JSON response to a Python dictionary
    data = json.loads(resp.content)
    with open('sub.json', 'w') as file:
        json_object = json.dumps(data, indent=4)
        file.write(json_object)
    # Get the list of form types
    form_types = data.get('filings', {}).get('recent', {}).get('form', [])
    # Initialize lists to hold the indices of 10-K and 10-Q filings
    indices_10k = [i for i, form in enumerate(form_types) if form == '10-K']
    indices_10q = [i for i, form in enumerate(form_types) if form == '10-Q']
    # Get the list of primary documents
    primary_docs = data.get('filings', {}).get('recent', {}).get('primaryDocument', [])

    # Get the primary documents of the 10-K filings
    primary_docs_10k = [primary_docs[i] for i in indices_10k]
    primary_docs_10q = [primary_docs[i] for i in indices_10q]
    # Get the list of accession numbers
    accession_numbers = data.get('filings', {}).get('recent', {}).get('accessionNumber', [])

    # Get the primary documents of the 10-K and 10-Q filings along with their accession numbers
    primary_docs_10k = [(accession_numbers[i], primary_docs[i], accession_numbers[i][11:13]) for i in indices_10k
                        if (accession_numbers[i][11:13] >= range[0]) and  (accession_numbers[i][11:13] <= range[1])]
    primary_docs_10q = [(accession_numbers[i], primary_docs[i], accession_numbers[i][11:13]) for i in indices_10q
                        if (accession_numbers[i][11:13] >= range[0]) and  (accession_numbers[i][11:13] <= range[1])]

    # Construct the URLs for the 10-K and 10-Q filings
    primary_docs_urls_10k = [(f'{base_url}/{num}/{acc_no.replace("-", "")}/{doc}', f'20{year}') for acc_no, doc,year in primary_docs_10k]
    primary_docs_urls_10q = [(f'{base_url}/{num}/{acc_no.replace("-", "")}/{doc}', f'20{year}') for acc_no, doc,year in primary_docs_10q]

    # Get the company's name
    #company_name = data.get('name')

    # Print the primary documents of the 10-K and 10-Q filings, and the company's name
    # Print the primary documents of the 10-K and 10-Q filings, the company's name, and the URLs
    if (form) == '10-K':

        form = '10k'
    elif (form) == '10-Q':
        form = '10q'
    url_dict= {

        '10k': primary_docs_urls_10k,
        '10q': primary_docs_urls_10q

    }


    print(url_dict[form])

    return url_dict[form]