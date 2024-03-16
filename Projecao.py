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
    ConsumoTotal = pd.read_csv(variables.ProjecaoPath + '\\ConsumoTotal.csv')
    ConsumoTotal.drop('Population', axis=1, inplace=True)
    ConsumoTotal.drop('PerCapitaConsumption', axis=1, inplace=True)

    GDP = pd.read_csv(variables.TransformPath + '\\GDP.csv')
    GDP.drop('Multiplier', axis=1, inplace=True)
    GDP.drop('GDP 2022 (2017 USD PPP)', axis=1, inplace=True)
    GDP.drop('GDP 2022 (2015 USD PPP)', axis=1, inplace=True)

    IntensidadeEnergetica = pd.merge(ConsumoTotal, GDP, how='inner', on=['Code','Year'])
    IntensidadeEnergetica['ConsumptionTotal'] = IntensidadeEnergetica['ConsumptionTotal'].astype(float)
    IntensidadeEnergetica['GDP 2015 PPP'] = IntensidadeEnergetica['GDP 2015 PPP'].astype(float)
    IntensidadeEnergetica['ConsumptionTotal'] = np.where(IntensidadeEnergetica['ConsumptionTotal'].isnull(), 0, IntensidadeEnergetica['ConsumptionTotal'])
    IntensidadeEnergetica['GDP 2015 PPP'] = np.where(IntensidadeEnergetica['GDP 2015 PPP'].isnull(), 0, IntensidadeEnergetica['GDP 2015 PPP'])
    IntensidadeEnergetica = IntensidadeEnergetica[IntensidadeEnergetica['GDP 2015 PPP'] > 0]

    IntensidadeEnergetica['IntensidadeEnergetica'] = (IntensidadeEnergetica['ConsumptionTotal']/IntensidadeEnergetica['GDP 2015 PPP'])*1000000000

    IntensidadeEnergetica['IntensidadeEnergetica'] = np.where(IntensidadeEnergetica['IntensidadeEnergetica'].isnull(), 0,IntensidadeEnergetica['IntensidadeEnergetica'])
    IntensidadeEnergetica['IntensidadeEnergetica'] = IntensidadeEnergetica['IntensidadeEnergetica'].astype(float)
    IntensidadeEnergetica = IntensidadeEnergetica[IntensidadeEnergetica['IntensidadeEnergetica'] > 0]

    ultimo_ano = ConsumoTotal.groupby('Code')['Year'].max()

    CoeficienteAjuste = (
        IntensidadeEnergetica
            .merge(ultimo_ano, on=['Code', 'Year'], how='inner')
            .assign(Rank=lambda x: x.groupby('Code').cumcount())
            .query('Rank < 10')
            .groupby('Code')['IntensidadeEnergetica']
            .mean()
            .reset_index()
            .rename(columns={'IntensidadeEnergetica': 'AvgLast10yrs'})
    )

    CoeficienteAjuste['AvgLast10yrs'] = CoeficienteAjuste['AvgLast10yrs'].astype(float)
    CoeficienteAjuste['GlobalAvg'] = CoeficienteAjuste['AvgLast10yrs'].mean()
    CoeficienteAjuste['GlobalAvg'] = CoeficienteAjuste['GlobalAvg'].astype(float)
    CoeficienteAjuste['CoeficienteAjuste'] = CoeficienteAjuste['AvgLast10yrs']/CoeficienteAjuste['GlobalAvg']
    CoeficienteAjuste['CoeficienteAjuste'] = CoeficienteAjuste['CoeficienteAjuste'].astype(float)


    IntensidadeEnergetica.to_csv(variables.ProjecaoPath + '\\IntensidadeEnergetica.csv', index=False)
    CoeficienteAjuste.to_csv(variables.ProjecaoPath + '\\CoeficienteAjuste.csv', index=False)

    print(CoeficienteAjuste)


def CrescimentoLimite():
    HIC = pd.read_excel(variables.ResourcesPath+'\\World Bank Countries Groups.xlsx',engine='openpyxl')
    HIC.drop('Economy', axis=1, inplace=True)
    HIC.drop('Region', axis=1, inplace=True)
    HIC.drop('Lending category', axis=1, inplace=True)
    HIC.drop('Unnamed: 5', axis=1, inplace=True)
    DC = HIC[HIC['Income group'] != "High income"]
    HIC = HIC[HIC['Income group'] == "High income"]

    HIC_Media10A = pd.read_csv(variables.ProjecaoPath + '\\Media10A.csv')
    HIC_Media10A = pd.merge(HIC_Media10A, HIC, how='inner', on=['Code'])
    HIC_Media10A = HIC_Media10A[HIC_Media10A['AvgLast10yrs'] > 0]

    HIC_Media10A_Total = HIC_Media10A['AvgLast10yrs'].mean()

    CoeficienteAjuste = pd.read_csv(variables.ProjecaoPath + '\\CoeficienteAjuste.csv')
    CoeficienteAjuste.drop('AvgLast10yrs', axis=1, inplace=True)
    CoeficienteAjuste.drop('GlobalAvg', axis=1, inplace=True)
    CoeficienteAjuste = pd.merge(CoeficienteAjuste, DC, how='inner', on=['Code'])
    CoeficienteAjuste.drop('Income group', axis=1, inplace=True)
    CoeficienteAjuste['HIC_AvgLast10yrs'] = HIC_Media10A['AvgLast10yrs'].mean()
    CoeficienteAjuste['HIC_AvgLast10yrs'] = CoeficienteAjuste['HIC_AvgLast10yrs'].astype(float)
    CoeficienteAjuste['MaxGrowth'] = CoeficienteAjuste['HIC_AvgLast10yrs']*CoeficienteAjuste['CoeficienteAjuste']
    CoeficienteAjuste['MaxGrowth'] = CoeficienteAjuste['MaxGrowth'].astype(float)
    CoeficienteAjuste.drop('CoeficienteAjuste', axis=1, inplace=True)
    CoeficienteAjuste.drop('HIC_AvgLast10yrs', axis=1, inplace=True)

    HIC_Media10A.drop('Income group', axis=1, inplace=True)
    HIC_Media10A.rename(columns={'AvgLast10yrs': 'MaxGrowth'}, inplace=True)

    CrescimentoLimite = pd.concat([HIC_Media10A,CoeficienteAjuste])
    CrescimentoLimite.to_csv(variables.ProjecaoPath + '\\CrescimentoLimite.csv', index=False)

    print(CrescimentoLimite)

#ConsumoPerCapita()
#FatordeAjuste()
CrescimentoLimite()