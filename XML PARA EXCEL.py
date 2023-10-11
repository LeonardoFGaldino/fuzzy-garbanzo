import os
import xml.etree.ElementTree as ET
import pandas as pd
from typing import List, Iterable
import tkinter as tk
from tkinter import filedialog



base_ncms = open('monofasia.csv', 'r', encoding='latin-1').readlines()
base_ncms = [linha.strip().split(',') for linha in base_ncms]
base_ncms = dict(base_ncms)



def classifica_ncm(ncm):
    if ncm not in base_ncms.keys():
        return 'TRIBUTADO'
    return base_ncms[ncm]


def selecionar_pasta():
    pasta_xml = filedialog.askdirectory(title="Selecionar Pasta com Arquivos XML")
    if pasta_xml:
        processar_arquivos_xml(pasta_xml)



pasta_xml = "C:\\Users\\Admin\\Downloads\\Arquivosxml"

tags_para_buscar = {
    'modelo': './/{*}ide/mod',
    'cnpj_emitente': './/{*}emit/CNPJ',
    'nome_emitente': './/{*}emit/xNome',
    'data_emissao': './/{*}ide/dEmi',
    'destinatario': './/{*}dest/xNome',
    'vl_total_produtos': './/{*}total/vCFe',
    'vl_total_lei_12741': './/{*}total/vCFeLei12741'
}

product_root = './/{*}det'
product_info = {
    'nome_prod': './/{*}prod/xProd',
    'ncm': './/{*}prod/NCM',
    'cfop': './/{*}prod/CFOP',
    'vl_prod': './/{*}prod/vProd',
    'vl_desconto': './/{*}prod/vDesc',
    'vl_item': './/{*}prod/vItem',
    'qnt_item': './/{*}prod/qCom',
    'cest': './/{*}prod/obsFiscoDet/xTextoDet'
}



def processar_arquivos_xml(pasta_xml):
    all_data = []

    for arquivo_xml in os.listdir(pasta_xml):
        if arquivo_xml.endswith(".xml"):
            caminho_completo = os.path.join(pasta_xml, arquivo_xml)
            tree = ET.parse(caminho_completo)
            root = tree.getroot()

            data_to_save = []

            for tag, xpath in tags_para_buscar.items():
                element = root.find(xpath)
                valor = element.text if element is not None else "Não encontrado"
                data_to_save.append(valor)

            for product_element in root.findall(product_root):
                product_data = []
                for info_xpath in product_info.values():
                    element = product_element.find(info_xpath)
                    valor = element.text if element is not None else "Não encontrado"
                    product_data.append(valor)
                all_data.append(data_to_save + product_data)

    column_names = list(tags_para_buscar.keys()) + list(product_info.keys())
    df = pd.DataFrame(all_data, columns=column_names)

    # Carregar o CSV e adicionar aos dados do DataFrame
    csv_filename = "monofasia.csv"
    csv_df = pd.read_csv(csv_filename)

    #df = pd.concat([df, csv_df], axis=1)  # Adicionar colunas do CSV ao DataFrame

    df['classificacao'] = df.ncm.map(classifica_ncm)

    output_excel = "leoarquivo4.xlsx"
    df.to_excel(output_excel, index=False)
    print(f"Arquivo Excel gerado: {output_excel}")

def main():
    root = tk.Tk()
    root.title("Processamento de Arquivos XML")

    btn_selecionar_pasta = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
    btn_selecionar_pasta.pack(padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
