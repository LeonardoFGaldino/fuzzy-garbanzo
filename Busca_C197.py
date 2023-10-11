import os
import pandas as pd

pasta_speds = 'C:\\'

linhas_c197 = []

for arquivo in os.listdir(pasta_speds):
    if arquivo.endswith('.txt'):
        with open(os.path.join(pasta_speds, arquivo), 'r', encoding='iso-8859-1') as sp:
            for linha in sp:
                if linha.startswith('|C197|'):
                    linhas_c197.append(linha.strip())

df = pd.DataFrame({'Linhas C197': linhas_c197})

df.to_excel('linhas_c197.xlsx', index=False)

print('Salvas em "linhas_c197.xlsx".')