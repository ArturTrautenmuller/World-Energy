import numpy as np
import pandas as pd
import variables

def TransformEletricity():
    # Eletricity
    Eletricity = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Coal.csv')
    Eletricity.rename(columns={'Electricity from coal (TWh)': 'Coal'}, inplace=True)

    Gas_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Gas.csv')
    Gas_prm.rename(columns={'Electricity from gas (TWh)': 'Gas'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Gas_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Gas_prm)

    Hydro_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Hydropower.csv')
    Hydro_prm.rename(columns={'Electricity from hydro (TWh)': 'Hydro'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Hydro_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Hydro_prm)

    Nuclear_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Nuclear.csv')
    Nuclear_prm.rename(columns={'Electricity from nuclear (TWh)': 'Nuclear'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Nuclear_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Nuclear_prm)

    Oil_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Oil.csv')
    Oil_prm.rename(columns={'Electricity from oil (TWh)': 'Oil'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Oil_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Oil_prm)

    Renewables_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Renewables.csv')
    Renewables_prm.rename(columns={'Electricity from renewables (TWh)': 'Renewables'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Renewables_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Renewables_prm)

    Solar_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Solar.csv')
    Solar_prm.rename(columns={'Electricity from solar (TWh)': 'Solar'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Solar_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Solar_prm)

    Wind_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Wind.csv')
    Wind_prm.rename(columns={'Electricity from wind (TWh)': 'Wind'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Wind_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Wind_prm)

    Eletricity['Code'] = np.where(Eletricity['Code'].isnull(), 'Regional', Eletricity['Code'])

    Eletricity['Coal'] = np.where(Eletricity['Coal'].isnull(), 0, Eletricity['Coal'])
    Eletricity['Coal'] = Eletricity['Coal'].astype(float)
    Eletricity['Gas'] = np.where(Eletricity['Gas'].isnull(), 0, Eletricity['Gas'])
    Eletricity['Gas'] = Eletricity['Gas'].astype(float)
    Eletricity['Hydro'] = np.where(Eletricity['Hydro'].isnull(), 0, Eletricity['Hydro'])
    Eletricity['Hydro'] = Eletricity['Hydro'].astype(float)
    Eletricity['Nuclear'] = np.where(Eletricity['Nuclear'].isnull(), 0, Eletricity['Nuclear'])
    Eletricity['Nuclear'] = Eletricity['Nuclear'].astype(float)
    Eletricity['Oil'] = np.where(Eletricity['Oil'].isnull(), 0, Eletricity['Oil'])
    Eletricity['Oil'] = Eletricity['Oil'].astype(float)
    Eletricity['Renewables'] = np.where(Eletricity['Renewables'].isnull(), 0, Eletricity['Renewables'])
    Eletricity['Renewables'] = Eletricity['Renewables'].astype(float)
    Eletricity['Solar'] = np.where(Eletricity['Solar'].isnull(), 0, Eletricity['Solar'])
    Eletricity['Solar'] = Eletricity['Solar'].astype(float)
    Eletricity['Wind'] = np.where(Eletricity['Wind'].isnull(), 0, Eletricity['Wind'])
    Eletricity['Wind'] = Eletricity['Wind'].astype(float)

    Eletricity['Other Renewables'] = Eletricity['Renewables'] - Eletricity['Solar'] - Eletricity['Wind'] - Eletricity['Hydro']
    Eletricity.drop('Renewables', axis=1, inplace=True)
    Eletricity = Eletricity.query('Code != "Regional" & Code != "OWID_WRL" & Year < 2023')

    #fix counrty name
    Countries = pd.read_csv(variables.ResourcesPath + '\\CountryMap.csv')
    Eletricity = pd.merge(Eletricity, Countries, how='left', on=['Entity'])
    Eletricity['Country'] = np.where(Eletricity['Country'].isnull(), Eletricity['Entity'], Eletricity['Country'])
    Eletricity.drop('Entity', axis=1, inplace=True)
    Eletricity.rename(columns={'Country': 'Entity'}, inplace=True)

    # EletricityFato

    EletricityFato = pd.melt(Eletricity, id_vars=['Entity', 'Code', 'Year'], var_name='Source', value_name='Consumption')
    SourceType = pd.read_csv(variables.ResourcesPath + '\\SourceClassification.csv')
    EletricityFato = pd.merge(EletricityFato, SourceType, how='left', on=['Source'])



    # Eletricity
    Population = pd.read_csv(variables.ExtractPath + '\\Population\\Population.csv')
    Population.drop('Country Code', axis=1, inplace=True)
    Population.drop('Indicator Name', axis=1, inplace=True)
    Population.drop('Indicator Code', axis=1, inplace=True)
    Population = pd.melt(Population, id_vars=['Country Name'], var_name='Year', value_name='Population')
    Population.rename(columns={'Country Name': 'Entity'}, inplace=True)
    Population['Population'] = np.where(Population['Population'].isnull(), 0, Population['Population'])
    Population = Population[Population['Year'] != 'Unnamed: 65']


    # Population.to_csv(variables.TransformPath+'\\Population.csv',index=False)

    Population['Year'] = Population['Year'].astype(int)
    Population = pd.merge(Population, Countries, how='left', on=['Entity'])
    Population['Country'] = np.where(Population['Country'].isnull(), Population['Entity'], Population['Country'])
    Population.drop('Entity', axis=1, inplace=True)
    Population.rename(columns={'Country': 'Entity'}, inplace=True)

    Eletricity = pd.merge(Eletricity, Population, how='left', on=['Entity', 'Year'])
    Eletricity['Population'] = np.where(Eletricity['Population'].isnull(), 0, Eletricity['Population'])

    Eletricity = Eletricity.query('Population > 0')
    EletricityFato.to_csv(variables.TransformPath + '\\EletricityFato.csv', index=False)

    GDP = pd.read_csv(variables.ME_TransformPath + '\\Fato.csv',usecols=['Ano','Pais','GDP_2010_dolar','GDP_PPP_2010_dolar'])
    GDP.rename(columns={'Pais': 'Entity'}, inplace=True)
    GDP.rename(columns={'Ano': 'Year'}, inplace=True)
    Eletricity = pd.merge(Eletricity, GDP, how='left', on=['Entity', 'Year'])

    Eletricity['GDP_2010_dolar'] = np.where(Eletricity['GDP_2010_dolar'].isnull(), 0, Eletricity['GDP_2010_dolar'])
    Eletricity['GDP_PPP_2010_dolar'] = np.where(Eletricity['GDP_PPP_2010_dolar'].isnull(), 0, Eletricity['GDP_PPP_2010_dolar'])

    Eletricity['Consumption'] = Eletricity['Coal'] + Eletricity['Gas'] + Eletricity['Oil'] + Eletricity['Nuclear'] + Eletricity['Solar'] + Eletricity['Wind'] + Eletricity['Hydro'] + Eletricity['Other Renewables']
    Eletricity.drop('Coal', axis=1, inplace=True)
    Eletricity.drop('Gas', axis=1, inplace=True)
    Eletricity.drop('Oil', axis=1, inplace=True)
    Eletricity.drop('Nuclear', axis=1, inplace=True)
    Eletricity.drop('Solar', axis=1, inplace=True)
    Eletricity.drop('Wind', axis=1, inplace=True)
    Eletricity.drop('Hydro', axis=1, inplace=True)
    Eletricity.drop('Other Renewables', axis=1, inplace=True)


    Eletricity.to_csv(variables.TransformPath + '\\Eletricity.csv', index=False)
