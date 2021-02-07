# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:59:35 2020

@author: Lais Nascimento
"""

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
import sys
import os

# ------------------------------------------------------------------


def retornaListaLinks(elementos):

    # lista de reposta para return
    resposta = []

    for elemento in elementos:

        # pega o link de cada elemento encontrado
        link = elemento.get_attribute("href")

        # adiciona o link na lista de reposta
        resposta.append(link)

    return resposta

# ------------------------------------------------------------------


def acha_lista(numero_de_tentativas, css_code_selector, driver):

    # cria uma lista vazia para dar return
    elementos = []

    # numero da tentativa atual
    tentativa_atual = 0

    # define um número limite de tentativas
    while tentativa_atual < numero_de_tentativas:

        try:
            elementos = driver.find_elements_by_class_name(
                "search-result__title")
            links = driver.find_elements_by_class_name("search-result__link")
            lista_links = retornaListaLinks(links)
            break

        # caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1

    manchetes = []
    links = []

    for elemento in elementos:
        manchetes.append(elemento.text)

    for l in lista_links:
        links.append(l)

    return manchetes, links

# ------------------------------------------------------------------


def soma_total(total, lista_projetos, lista_links):

    for i in range(len(lista_de_links)):

        # pega o projeto atual
        projeto = lista_projetos[i]

        # pega o link do projeto atual
        link = lista_links[i]

        # cria um json do projeto
        json = {'projeto': projeto, 'link': link}

        # adiciona na lista de total
        total.append(json)

    return total

# ------------------------------------------------------------------

def projetos_antigos(url):
    if str(sys.argv[3]) == "production":
        client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
    else:
        client = MongoClient(str(mongo_url))

    db = client.get_database('sites')
    collection = db.go_lab
    lista = list(collection.find())

    resposta = []
    for document in lista:
        resposta.append(document)

    return resposta

# ------------------------------------------------------------------


def atualizaBackUP(lista_com_links, url, boolean):

    if str(boolean) == "true" and len(lista_com_links) > 0:
        if str(sys.argv[3]) == "production":
            client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
        else:
            client = MongoClient(str(mongo_url))

        db = client.get_database('sites')  # pega o database
        collection = db.go_lab  # pega a collection desejada

        collection.insert_many(lista_com_links)  # atualiza os documentos
    else:
        pass

    return

# ----------------------------------------------


def links_novos(antigos, potenciais):

    #lista que não terá o _id
    antigo_fake = []

    for documento in antigos:
        json = {'projeto': documento['projeto'], 'link': documento['link']}
        antigo_fake.append(json)

    # lista que será usada para armazenar os projetos novos
    novos = []

    for json in potenciais:

        # verifica se o json está na lista de antigos
        if json not in antigo_fake:

            # adiciona na lista de novos projetos
            novos.append(json)

    return novos

# ----------------------------------------------


def apenas_links(lista):

    # cria uma lista de resposta
    resposta = []

    for json in lista:

        # pega o link do projeto
        link_do_projeto = json["link"]

        # adiciona na lista de resposta
        resposta.append(link_do_projeto)

    return resposta

# ----------------------------------------------


if(str(sys.argv[3]) == "production"):
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

else:
    # cria o webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

# página atual
pag = 1

# total de projetos
total = []

while pag <= 12:

    # determina a url do site desejado
    url = "https://golab.bsg.ox.ac.uk/knowledge-bank/indigo-data-and-visualisation/impact-bond-dataset-v2/?page=" + str(pag)

    # pega o conteúdo da url
    driver.get(url)

    # tempo para carregar a página inteira
    time.sleep(10)

    # pega os novos projetos
    lista_de_projetos, lista_de_links = acha_lista(
        1000, "#ngo > div.search-results > div", driver)

    # soma os novos projetos na lista de total
    total = soma_total(total, lista_de_projetos, lista_de_links)

    # vai para a próxima página
    pag += 1

# fecha a janela aberta
driver.close()

# pega os projetos antigos
projetos_antigos = projetos_antigos(sys.argv[1])

# pega os novos projetos
novos_projetos = links_novos(projetos_antigos, total)

# apenas os links dos projetos novos
resposta_final = apenas_links(novos_projetos)

# atualiza o mongo Atlas
update = atualizaBackUP(novos_projetos, sys.argv[1], sys.argv[2])

print(resposta_final)
sys.stdout.flush()