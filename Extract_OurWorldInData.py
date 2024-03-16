import requests
import json
import pandas as pd
import variables


indicator_list = pd.read_excel(variables.ResourcesPath+'\\OurWorldInData_Indicadores.xlsx',engine='openpyxl')


for index, indicator in indicator_list.iterrows():
    print(f"Extraindo: ({indicator['Indicador']})")
    url = f"https://api.ourworldindata.org/v1/indicators/{indicator['Codigo']}.data.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).text

    data = json.loads(response)

    entities = data['entities']
    years = data['years']
    values = data['values']

    columns = {'fonte': indicator['Dimensao'],'entities': entities, 'years': years, 'values': values}

    df = pd.DataFrame(columns)

    df.to_csv(variables.ExtractPath + indicator['Arquivo'], index=False)


