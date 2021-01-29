import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time
import sys
import os

# ----------------------------------------------


def transforma_data(url):
    client = MongoClient(str(url))
    db = client.get_database('sites')
    collection = db.instiglio
    lista = list(collection.find())

    resposta = {"source": []}
    for document in lista:
        resposta['source'].append(document['source'])

    return resposta

# ----------------------------------------------


def retornaListaLinks(elementos):

    # lista de reposta para return
    resposta = []

    for elemento in elementos:

        # pega o link de cada elemento encontrado
        link = elemento.get_attribute("href")

        # adiciona o link na lista de reposta
        resposta.append(link)

    return resposta

# ----------------------------------------------


def pegaListaAntigos(data_to_df):

    # cria lista de resposta para return
    resposta = []

    # cria um dataframe
    df = pd.DataFrame(data=data_to_df)

    # adiciona todos os links antigos na lista de resposta
    df["source"].apply(lambda x: resposta.append(x))

    return resposta

# ----------------------------------------------


def comparaListas(lista1, lista2):

    # cria lista de resposta para return
    resposta = []

    # vamos comparar cada elemento das duas lista
    for elemento in lista1:

        # se o elemento da lista1 não estiver na lista2...
        if elemento not in lista2:

            # adiciona o elemento novo na lista de resposta
            resposta.append(elemento)

        # se o elemento já estiver na outra lista, o link é antigo
        else:
            pass

    return resposta

# ----------------------------------------------


def atualizaBackUP(lista_com_links, url, boolean):

    if str(boolean) == "true" and len(lista_com_links) > 0:
        client = MongoClient(str(url))  # conecta com o banco de dados
        db = client.get_database('sites')  # pega o database
        collection = db.instiglio  # pega a collection desejada

        lista_to_insert = []  # lista que amarzenará os novos documentos

        for id_ in lista_com_links:

            # cria uma nova linha com o id novo
            new_row = {"source": id_}

            # adiciona o novo documento
            lista_to_insert.append(new_row)

        collection.insert_many(lista_to_insert)  # atualiza os documentos
    else:
        pass

    return

# ----------------------------------------------


# cria a pasta do projeto
path = os.path.dirname(__file__) + "/Backup/instiglio.xlsx"

# determina a url do site desejado
url = "https://www.instiglio.org/en/projects/"

# cria o webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# pega o conteúdo da url
driver.get(url)

# tempo para carregar a página inteira
time.sleep(2)

# encontra a lista de elementos
elementos = driver.find_elements_by_css_selector(".wpb_wrapper [href]")

# cria lista de links encontrados
lista_links = retornaListaLinks(elementos)

# json transformado para ser usado como dataFrame
json_transfomado = transforma_data(sys.argv[1])

# cria a lista de antigos:
lista_antigos = pegaListaAntigos(json_transfomado)

# cria a lista com os links novos
lista_novos_links = comparaListas(lista_links, lista_antigos)

# atualiza o arquivo de backup
atualizaBackUP(lista_novos_links, sys.argv[1], sys.argv[2])

print(lista_novos_links)
sys.stdout.flush()
