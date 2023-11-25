import numpy as np
import pandas as pd
import variables
import json
import csv
import requests

countries_df = pd.read_csv(variables.ResourcesPath+'\\Countries.csv')

# Loop para cada valor na coluna 'Cod'
for country_code in countries_df['Cod']:
    # Coloque aqui o código que você deseja executar para cada valor de 'Cod'
    print(f"Processando para: {country_code}")

    with open(variables.ExtractPath + f'\\Projeção População\\population_{country_code}.csv', 'w', newline='') as csvfile:
        # Define the CSV writer and write the header
        fieldnames = ['Code', 'Year', 'Population']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()



        for year in range(1950, 2101):
            url = f'https://www.populationpyramid.net/api/pp/{country_code}/{year}/'

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload).text
            population = json.loads(response)['population']
            writer.writerow({'Code': str(country_code), 'Year': year, 'Population': population})

'''
for year in range(1950, 2101):
    code = 76
    url = f'https://www.populationpyramid.net/api/pp/{code}/{year}/?csv=true'
    filename = variables.ExtractPath+f'\\Projeção População\\population_{code}_{year}.csv'

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Download concluído para o ano {year}!')
    else:
        print(f'Ocorreu um erro durante o download para o ano {year}.')
'''