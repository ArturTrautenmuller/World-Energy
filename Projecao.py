import numpy as np
import pandas as pd
import variables

def ConsumoPerCapita():
    ConsumoTotal = pd.read_csv(variables.TransformPath + '\\Fato.csv')
    ConsumoTotal = ConsumoTotal.groupby(['Code', 'Year'])['Consumption'].sum().reset_index()

    # Renomeando a coluna 'Consumption' para 'ConsumptionTotal'
    ConsumoTotal.rename(columns={'Consumption': 'ConsumptionTotal'}, inplace=True)
    ConsumoTotal['ConsumptionTotal'] = ConsumoTotal['ConsumptionTotal'].astype(float)
    Population = pd.read_csv(variables.TransformPath + '\\Population.csv')
    ConsumoTotal = pd.merge(ConsumoTotal, Population, how='left', on=['Code','Year'])
    ConsumoTotal['Population'] = ConsumoTotal['Population'].astype(float)
    ConsumoTotal['PerCapitaConsumption'] = (ConsumoTotal['ConsumptionTotal']/ConsumoTotal['Population'])*1000000
    ConsumoTotal['PerCapitaConsumption'] = ConsumoTotal['PerCapitaConsumption'].astype(float)

    ConsumoTotal['PerCapitaConsumption'] = np.where(ConsumoTotal['PerCapitaConsumption'].isnull(), 0,ConsumoTotal['PerCapitaConsumption'])

    ultimo_ano = ConsumoTotal.groupby('Code')['Year'].max()
    primeiro_ano = ConsumoTotal.groupby('Code')['Year'].min()

    Media10A = (
        ConsumoTotal
            .merge(ultimo_ano, on=['Code', 'Year'], how='inner')
            .assign(Rank=lambda x: x.groupby('Code').cumcount())
            .query('Rank < 10')
            .groupby('Code')['PerCapitaConsumption']
            .mean()
            .reset_index()
            .rename(columns={'PerCapitaConsumption': 'AvgLast10yrs'})
    )

    Media10A['AvgLast10yrs'] = Media10A['AvgLast10yrs'].astype(float)

    consumo_inicio  = pd.merge(ConsumoTotal, primeiro_ano, how='inner', on=['Code','Year'])
    consumo_inicio.drop('ConsumptionTotal', axis=1, inplace=True)
    consumo_inicio.drop('Population', axis=1, inplace=True)
    consumo_inicio.rename(columns={'Year': 'FirstYear'}, inplace=True)
    consumo_inicio.rename(columns={'PerCapitaConsumption': 'FirstPerCapitaConsumption'}, inplace=True)
    consumo_inicio['FirstYear'] = consumo_inicio['FirstYear'].astype(int)

    consumo_final = pd.merge(ConsumoTotal, ultimo_ano, how='inner', on=['Code', 'Year'])
    consumo_final.drop('ConsumptionTotal', axis=1, inplace=True)
    consumo_final.drop('Population', axis=1, inplace=True)
    consumo_final.rename(columns={'Year': 'LastYear'}, inplace=True)
    consumo_final.rename(columns={'PerCapitaConsumption': 'LastPerCapitaConsumption'}, inplace=True)
    consumo_final['LastYear'] = consumo_final['LastYear'].astype(int)

    CrescimentoMedio = pd.merge(consumo_inicio, consumo_final, how='inner', on=['Code'])
    CrescimentoMedio['TotalGrowth'] = CrescimentoMedio['LastPerCapitaConsumption'] - CrescimentoMedio['FirstPerCapitaConsumption']
    CrescimentoMedio['Period'] = CrescimentoMedio['LastYear'] - CrescimentoMedio['FirstYear']
    CrescimentoMedio['AvgGrowth'] = CrescimentoMedio['TotalGrowth']/CrescimentoMedio['Period']
    CrescimentoMedio['AvgGrowth'] = np.where(CrescimentoMedio['AvgGrowth'].isnull(), 0,CrescimentoMedio['AvgGrowth'])
    CrescimentoMedio['AvgGrowth'] = CrescimentoMedio['AvgGrowth'].astype(float)




    ConsumoTotal.to_csv(variables.ProjecaoPath + '\\ConsumoTotal.csv', index=False)
    Media10A.to_csv(variables.ProjecaoPath + '\\Media10A.csv', index=False)
    CrescimentoMedio.to_csv(variables.ProjecaoPath + '\\CrescimentoMedio.csv', index=False)
    print(CrescimentoMedio)

def FatordeAjuste():
    HIC = pd.read_excel(variables.ResourcesPath+'\\World Bank Countries Groups.xlsx',engine='openpyxl')
    HIC.drop('Economy', axis=1, inplace=True)
    HIC.drop('Region', axis=1, inplace=True)
    HIC.drop('Lending category', axis=1, inplace=True)
    HIC.drop('Unnamed: 5', axis=1, inplace=True)
    HIC = HIC[HIC['Income group'] == "High income"]

    HIC_Media10A = pd.read_csv(variables.ProjecaoPath + '\\Media10A.csv')

    print(HIC)

#ConsumoPerCapita()
FatordeAjuste()
