import numpy as np
import pandas as pd
import variables


def TransformPrimary():
    Coal = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Coal.csv')
    Gas = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Gas.csv')
    Oil = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Oil.csv')
    Nuclear = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Nuclear.csv')
    Hydro = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Hydropower.csv')
    Solar = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Solar.csv')
    Wind = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Wind.csv')

    Primary = pd.concat([Coal, Gas, Oil,Nuclear,Hydro,Solar,Wind], ignore_index=True)



    Renewables = pd.read_csv(variables.ExtractPath + '\\Source\\Primary\\Renewables.csv')
    Renewables.rename(columns={'values': 'Renewables'}, inplace=True)
    Renewables.drop('fonte', axis=1, inplace=True)
    Solar.rename(columns={'values': 'Solar'}, inplace=True)
    Solar.drop('fonte', axis=1, inplace=True)
    Wind.rename(columns={'values': 'Wind'}, inplace=True)
    Wind.drop('fonte', axis=1, inplace=True)
    Hydro.rename(columns={'values': 'Hydro'}, inplace=True)
    Hydro.drop('fonte', axis=1, inplace=True)

    Renewables = pd.merge(Renewables, Solar, how='outer', on=['entities', 'years'])
    Renewables = pd.merge(Renewables, Wind, how='outer', on=['entities', 'years'])
    Renewables = pd.merge(Renewables, Hydro, how='outer', on=['entities', 'years'])
    Renewables['values'] = Renewables['Renewables'] - Renewables['Solar'] - Renewables['Wind'] - Renewables['Hydro']
    Renewables['fonte'] = 'Other Renewables'

    Renewables.drop('Solar', axis=1, inplace=True)
    Renewables.drop('Wind', axis=1, inplace=True)
    Renewables.drop('Hydro', axis=1, inplace=True)
    Renewables.drop('Renewables', axis=1, inplace=True)

    Primary = pd.concat([Primary,Renewables], ignore_index=True)

    Primary.rename(columns={'values': 'Consumption'}, inplace=True)
    Primary.rename(columns={'fonte': 'Source'}, inplace=True)
    Primary.rename(columns={'entities': 'CodeNumeric'}, inplace=True)
    Primary.rename(columns={'years': 'Year'}, inplace=True)

    Primary['Consumption'] = np.where(Primary['Consumption'].isnull(), 0, Primary['Consumption'])
    Primary['Consumption'] = Primary['Consumption'].astype(float)

    SourceType = pd.read_csv(variables.ResourcesPath + '\\SourceClassification.csv')
    Primary = pd.merge(Primary, SourceType, how='left', on=['Source'])

    CountriesOWD = pd.read_csv(variables.ResourcesPath + '\\OurWorldInData_Countries.csv')
    CountriesOWD.rename(columns={'id': 'CodeNumeric'}, inplace=True)
    CountriesOWD.rename(columns={'code': 'Code'}, inplace=True)
    CountriesOWD.drop('name', axis=1, inplace=True)
    Primary = pd.merge(Primary, CountriesOWD, how='left', on=['CodeNumeric'])
    Primary.drop('CodeNumeric', axis=1, inplace=True)

    Primary = Primary.dropna(subset=['Code'])


    Countries = pd.read_csv(variables.ResourcesPath + '\\Countries - ISO.csv')
    Countries.drop('Alpha2', axis=1, inplace=True)
    Countries.drop('Code', axis=1, inplace=True)
    Countries.rename(columns={'Alpha3': 'Code'}, inplace=True)
    Countries.rename(columns={'Country': 'Entity'}, inplace=True)
    Primary = pd.merge(Primary, Countries, how='left', on=['Code'])




    print(Primary)
    Primary.to_csv(variables.TransformPath + '\\PrimaryFato.csv', index=False)


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



    Primary = pd.merge(Primary, Population, how='left', on=['Entity', 'Year'])
    Primary['Population'] = np.where(Primary['Population'].isnull(), 0, Primary['Population'])

    Primary = Primary.query('Population > 0')

    GDP = pd.read_csv(variables.ME_TransformPath + '\\Fato.csv',
                      usecols=['Ano', 'Pais', 'GDP_2010_dolar', 'GDP_PPP_2010_dolar'])
    GDP.rename(columns={'Pais': 'Entity'}, inplace=True)
    GDP.rename(columns={'Ano': 'Year'}, inplace=True)
    Primary = pd.merge(Primary, GDP, how='left', on=['Entity', 'Year'])

    Primary['GDP_2010_dolar'] = np.where(Primary['GDP_2010_dolar'].isnull(), 0, Primary['GDP_2010_dolar'])
    Primary['GDP_PPP_2010_dolar'] = np.where(Primary['GDP_PPP_2010_dolar'].isnull(), 0, Primary['GDP_PPP_2010_dolar'])

    Primary.to_csv(variables.TransformPath + '\\Primary.csv', index=False)




def TransformEletricity():
    Coal = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Coal.csv')
    Gas = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Gas.csv')
    Oil = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Oil.csv')
    Nuclear = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Nuclear.csv')
    Hydro = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Hydropower.csv')
    Solar = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Solar.csv')
    Wind = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Wind.csv')

    Eletricity = pd.concat([Coal, Gas, Oil,Nuclear,Hydro,Solar,Wind], ignore_index=True)



    Renewables = pd.read_csv(variables.ExtractPath + '\\Source\\Eletricity\\Renewables.csv')
    Renewables.rename(columns={'values': 'Renewables'}, inplace=True)
    Renewables.drop('fonte', axis=1, inplace=True)
    Solar.rename(columns={'values': 'Solar'}, inplace=True)
    Solar.drop('fonte', axis=1, inplace=True)
    Wind.rename(columns={'values': 'Wind'}, inplace=True)
    Wind.drop('fonte', axis=1, inplace=True)
    Hydro.rename(columns={'values': 'Hydro'}, inplace=True)
    Hydro.drop('fonte', axis=1, inplace=True)

    Renewables = pd.merge(Renewables, Solar, how='outer', on=['entities', 'years'])
    Renewables = pd.merge(Renewables, Wind, how='outer', on=['entities', 'years'])
    Renewables = pd.merge(Renewables, Hydro, how='outer', on=['entities', 'years'])
    Renewables['values'] = Renewables['Renewables'] - Renewables['Solar'] - Renewables['Wind'] - Renewables['Hydro']
    Renewables['fonte'] = 'Other Renewables'

    Renewables.drop('Solar', axis=1, inplace=True)
    Renewables.drop('Wind', axis=1, inplace=True)
    Renewables.drop('Hydro', axis=1, inplace=True)
    Renewables.drop('Renewables', axis=1, inplace=True)

    Eletricity = pd.concat([Eletricity,Renewables], ignore_index=True)

    Eletricity.rename(columns={'values': 'Consumption'}, inplace=True)
    Eletricity.rename(columns={'fonte': 'Source'}, inplace=True)
    Eletricity.rename(columns={'entities': 'CodeNumeric'}, inplace=True)
    Eletricity.rename(columns={'years': 'Year'}, inplace=True)

    Eletricity['Consumption'] = np.where(Eletricity['Consumption'].isnull(), 0, Eletricity['Consumption'])
    Eletricity['Consumption'] = Eletricity['Consumption'].astype(float)

    SourceType = pd.read_csv(variables.ResourcesPath + '\\SourceClassification.csv')
    Eletricity = pd.merge(Eletricity, SourceType, how='left', on=['Source'])

    CountriesOWD = pd.read_csv(variables.ResourcesPath + '\\OurWorldInData_Countries.csv')
    CountriesOWD.rename(columns={'id': 'CodeNumeric'}, inplace=True)
    CountriesOWD.rename(columns={'code': 'Code'}, inplace=True)
    CountriesOWD.drop('name', axis=1, inplace=True)
    Eletricity = pd.merge(Eletricity, CountriesOWD, how='left', on=['CodeNumeric'])

    Eletricity = Eletricity.dropna(subset=['Code'])


    Countries = pd.read_csv(variables.ResourcesPath + '\\Countries - ISO.csv')
    Countries.drop('Alpha2', axis=1, inplace=True)
    Countries.drop('Code', axis=1, inplace=True)
    Countries.rename(columns={'Alpha3': 'Code'}, inplace=True)
    Countries.rename(columns={'Country': 'Entity'}, inplace=True)
    Eletricity = pd.merge(Eletricity, Countries, how='left', on=['Code'])


    print(Eletricity)
    Eletricity.to_csv(variables.TransformPath + '\\EletricityFato.csv', index=False)

def Population():
    Population = pd.read_csv(variables.ExtractPath + '\\Population\\Population.csv')
    Population.drop('Country Name', axis=1, inplace=True)
    Population.drop('Indicator Name', axis=1, inplace=True)
    Population.drop('Indicator Code', axis=1, inplace=True)
    Population = pd.melt(Population, id_vars=['Country Code'], var_name='Year', value_name='Population')
    Population.rename(columns={'Country Code': 'Code'}, inplace=True)
    Population['Population'] = np.where(Population['Population'].isnull(), 0, Population['Population'])
    Population = Population[Population['Year'] != 'Unnamed: 65']

    # Population.to_csv(variables.TransformPath+'\\Population.csv',index=False)
    countries_df = pd.read_csv(variables.ResourcesPath + '\\Countries.csv')
    countries_df.rename(columns={'Cod.A3': 'Code'}, inplace=True)
    countries_df.drop('Cod.A2', axis=1, inplace=True)
    countries_df.drop('Cod', axis=1, inplace=True)
    Population = pd.merge(Population, countries_df, how='inner', on=['Code'])

    Population['Year'] = Population['Year'].astype(int)
    Population.to_csv(variables.TransformPath + '\\Population.csv', index=False)


def Geral():
    PrimaryFato = pd.read_csv(variables.TransformPath + '\\PrimaryFato.csv')
    EletricityFato = pd.read_csv(variables.TransformPath + '\\EletricityFato.csv')

   # PrimaryFato.drop('Population', axis=1, inplace=True)
   # EletricityFato.drop('Population', axis=1, inplace=True)

    EletricityFato.rename(columns={'Consumption': 'Consumption_Eletricity'}, inplace=True)

    Fato = pd.merge(PrimaryFato, EletricityFato, how='outer', on=['Year','Source','Classification','Entity','Code'])
    Fato['Consumption'] = np.where(Fato['Consumption'].isnull(), 0, Fato['Consumption'])
    Fato['Consumption_Eletricity'] = np.where(Fato['Consumption_Eletricity'].isnull(), 0, Fato['Consumption_Eletricity'])


    Fato.to_csv(variables.TransformPath + '\\Fato.csv', index=False)

def CO2_EMISSION():
    Coal = pd.read_csv(variables.ExtractPath + '\\Emissao CO2\\Coal.csv')
    Oil = pd.read_csv(variables.ExtractPath + '\\Emissao CO2\\Oil.csv')
    Gas = pd.read_csv(variables.ExtractPath + '\\Emissao CO2\\Gas.csv')

    CO2 = pd.concat([Coal, Gas, Oil], ignore_index=True)
    CO2.rename(columns={'fonte': 'Source'}, inplace=True)
    CO2.rename(columns={'entities': 'CodeNumeric'}, inplace=True)
    CO2.rename(columns={'years': 'Year'}, inplace=True)
    CO2.rename(columns={'values': 'CO2 Emission'}, inplace=True)

    CountriesOWD = pd.read_csv(variables.ResourcesPath + '\\OurWorldInData_Countries.csv')
    CountriesOWD.rename(columns={'id': 'CodeNumeric'}, inplace=True)
    CountriesOWD.rename(columns={'code': 'Code'}, inplace=True)
    CountriesOWD.drop('name', axis=1, inplace=True)
    CO2 = pd.merge(CO2, CountriesOWD, how='left', on=['CodeNumeric'])

    CO2 = CO2.dropna(subset=['Code'])
    CO2['CO2 Emission'] = CO2['CO2 Emission'].astype(float)
    CO2.to_csv(variables.TransformPath + '\\CO2 Emission.csv', index=False)
    
    
Population()
TransformPrimary()
TransformEletricity()
Geral()
CO2_EMISSION()