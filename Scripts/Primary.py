import numpy as np
import pandas as pd
import variables

def TransformPrimary():
    # Primary
    Primary = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Coal.csv')
    print(Primary)
    Primary.rename(columns={'Coal Consumption - TWh': 'Coal'}, inplace=True)

    Gas_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Gas.csv')
    Gas_prm.rename(columns={'Gas Consumption - TWh': 'Gas'}, inplace=True)
    Primary = pd.merge(Primary, Gas_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Gas_prm)

    Hydro_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Hydropower.csv')
    Hydro_prm.rename(columns={'Hydro (TWh - equivalent)': 'Hydro'}, inplace=True)
    Primary = pd.merge(Primary, Hydro_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Hydro_prm)

    Nuclear_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Nuclear.csv')
    Nuclear_prm.rename(columns={'Nuclear (TWh - equivalent)': 'Nuclear'}, inplace=True)
    Primary = pd.merge(Primary, Nuclear_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Nuclear_prm)

    Oil_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Oil.csv')
    Oil_prm.rename(columns={'Oil Consumption - TWh': 'Oil'}, inplace=True)
    Primary = pd.merge(Primary, Oil_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Oil_prm)

    Renewables_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Renewables.csv')
    Renewables_prm.rename(columns={'Renewables (TWh - equivalent)': 'Renewables'}, inplace=True)
    Primary = pd.merge(Primary, Renewables_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Renewables_prm)

    Solar_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Solar.csv')
    Solar_prm.rename(columns={'Solar (TWh - equivalent)': 'Solar'}, inplace=True)
    Primary = pd.merge(Primary, Solar_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Solar_prm)

    Wind_prm = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Wind.csv')
    Wind_prm.rename(columns={'Wind (TWh - equivalent)': 'Wind'}, inplace=True)
    Primary = pd.merge(Primary, Wind_prm, how='outer', on=['Entity', 'Code', 'Year'])
    del (Wind_prm)

    Primary['Code'] = np.where(Primary['Code'].isnull(), 'Regional', Primary['Code'])



    Primary['Coal'] = np.where(Primary['Coal'].isnull(), 0, Primary['Coal'])
    Primary['Coal'] = Primary['Coal'].astype(float)
    Primary['Gas'] = np.where(Primary['Gas'].isnull(), 0, Primary['Gas'])
    Primary['Gas'] = Primary['Gas'].astype(float)
    Primary['Hydro'] = np.where(Primary['Hydro'].isnull(), 0, Primary['Hydro'])
    Primary['Hydro'] = Primary['Hydro'].astype(float)
    Primary['Nuclear'] = np.where(Primary['Nuclear'].isnull(), 0, Primary['Nuclear'])
    Primary['Nuclear'] = Primary['Nuclear'].astype(float)
    Primary['Oil'] = np.where(Primary['Oil'].isnull(), 0, Primary['Oil'])
    Primary['Oil'] = Primary['Oil'].astype(float)
    Primary['Renewables'] = np.where(Primary['Renewables'].isnull(), 0, Primary['Renewables'])
    Primary['Renewables'] = Primary['Renewables'].astype(float)
    Primary['Solar'] = np.where(Primary['Solar'].isnull(), 0, Primary['Solar'])
    Primary['Solar'] = Primary['Solar'].astype(float)
    Primary['Wind'] = np.where(Primary['Wind'].isnull(), 0, Primary['Wind'])
    Primary['Wind'] = Primary['Wind'].astype(float)

    Primary['Other Renewables'] = Primary['Renewables'] - Primary['Solar'] - Primary['Wind'] - Primary['Hydro']
    Primary.drop('Renewables', axis=1, inplace=True)
    Primary = Primary.query('Code != "Regional" & Code != "OWID_WRL"')

    #fix counrty name
    Countries = pd.read_csv(variables.ResourcesPath + '\\CountryMap.csv')
    Primary = pd.merge(Primary, Countries, how='left', on=['Entity'])
    Primary['Country'] = np.where(Primary['Country'].isnull(), Primary['Entity'], Primary['Country'])
    Primary.drop('Entity', axis=1, inplace=True)
    Primary.rename(columns={'Country': 'Entity'}, inplace=True)



    # PrimaryFato

    PrimaryFato = pd.melt(Primary, id_vars=['Entity', 'Code', 'Year'], var_name='Source', value_name='Consumption')
    SourceType = pd.read_csv(variables.ResourcesPath + '\\SourceClassification.csv')
    PrimaryFato = pd.merge(PrimaryFato, SourceType, how='left', on=['Source'])



    # Primary
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
    # fix counrty name

    Population = pd.merge(Population, Countries, how='left', on=['Entity'])
    Population['Country'] = np.where(Population['Country'].isnull(), Population['Entity'], Population['Country'])
    Population.drop('Entity', axis=1, inplace=True)
    Population.rename(columns={'Country': 'Entity'}, inplace=True)


    Primary = pd.merge(Primary, Population, how='left', on=['Entity', 'Year'])
    Primary['Population'] = np.where(Primary['Population'].isnull(), 0, Primary['Population'])

    Primary = Primary.query('Population > 0')
    PrimaryFato.to_csv(variables.TransformPath + '\\PrimaryFato.csv', index=False)

    GDP = pd.read_csv(variables.ME_TransformPath + '\\Fato.csv',
                      usecols=['Ano', 'Pais', 'GDP_2010_dolar', 'GDP_PPP_2010_dolar'])
    GDP.rename(columns={'Pais': 'Entity'}, inplace=True)
    GDP.rename(columns={'Ano': 'Year'}, inplace=True)
    Primary = pd.merge(Primary, GDP, how='left', on=['Entity', 'Year'])

    Primary['GDP_2010_dolar'] = np.where(Primary['GDP_2010_dolar'].isnull(), 0, Primary['GDP_2010_dolar'])
    Primary['GDP_PPP_2010_dolar'] = np.where(Primary['GDP_PPP_2010_dolar'].isnull(), 0, Primary['GDP_PPP_2010_dolar'])

    Primary['Consumption'] = Primary['Coal'] + Primary['Gas'] + Primary['Oil'] + Primary['Nuclear'] + Primary['Solar'] + Primary['Wind'] + Primary['Hydro'] + Primary['Other Renewables']
    Primary.drop('Coal', axis=1, inplace=True)
    Primary.drop('Gas', axis=1, inplace=True)
    Primary.drop('Oil', axis=1, inplace=True)
    Primary.drop('Nuclear', axis=1, inplace=True)
    Primary.drop('Solar', axis=1, inplace=True)
    Primary.drop('Wind', axis=1, inplace=True)
    Primary.drop('Hydro', axis=1, inplace=True)
    Primary.drop('Other Renewables', axis=1, inplace=True)


    Primary.to_csv(variables.TransformPath + '\\Primary.csv', index=False)
