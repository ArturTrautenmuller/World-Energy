import numpy as np
import pandas as pd
import variables

def Geral():
    PrimaryFato = pd.read_csv(variables.TransformPath + '\\PrimaryFato.csv')
    EletricityFato = pd.read_csv(variables.TransformPath + '\\EletricityFato.csv')

   # PrimaryFato.drop('Population', axis=1, inplace=True)
   # EletricityFato.drop('Population', axis=1, inplace=True)

    EletricityFato.rename(columns={'Consumption': 'Consumption_Eletricity'}, inplace=True)

    Fato = pd.merge(PrimaryFato, EletricityFato, how='outer', on=['Entity', 'Code', 'Year','Source','Classification'])
    Fato['Consumption'] = np.where(Fato['Consumption'].isnull(), 0, Fato['Consumption'])
    Fato['Consumption_Eletricity'] = np.where(Fato['Consumption_Eletricity'].isnull(), 0, Fato['Consumption_Eletricity'])
    print(Fato)

    Fato.to_csv(variables.TransformPath + '\\Fato.csv', index=False)

