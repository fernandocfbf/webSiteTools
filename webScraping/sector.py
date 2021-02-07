import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import sys
import time
import pandas as pd

# ------------------------------------------------------------------------------

def acha_lista(numero_de_tentativas, css_code_selector, driver):

    # cria uma lista vazia para amarzenar os elementos do HTML
    elementos = []

    # cria uma lista para return
    manchetes = []

    # numero da tentativa atual
    tentativa_atual = 0

    # define um número limite de tentativas
    elementos = []
    acabou = False
    l = 1
    i = 1
    while tentativa_atual < numero_de_tentativas:
        try:
            while l != 0:
                elemento = driver.find_elements_by_xpath(
                    '/html/body/div[1]/div[3]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[1]')
                l = len(elemento)
                elementos.append(elemento)
                i = i+2
            break

        # caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1

    for l_elemento in elementos:
        for e in l_elemento:
            manchetes.append(e.text)

    return manchetes

# ------------------------------------------------------------------------------

def transforma_data(url):
    if str(sys.argv[3]) == "production":
        client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
    else:
        client = MongoClient(str(mongo_url))

    db = client.get_database('sites')
    collection = db.sector
    lista = list(collection.find())

    lista_resposta = []

    for document in lista:
        lista_resposta.append(document['source'])

    return lista_resposta

# ------------------------------------------------------------------------------

def compara(lista_projetos, lista_antigos):

    #cria uma lista vazia para return
    lista_novos = []

    for projeto in lista_de_projetos:

        #se o projeto não está nos registros
        if projeto not in lista_antigos:

            #adiciona na lista de resposta
            lista_novos.append(projeto)
    
    return lista_novos

# ------------------------------------------------------------------------------

def atualizaBackUP(lista_com_ids, url, boolean):

    if str(boolean) == "true" and len(lista_com_ids) > 0:
        if str(sys.argv[3]) == "production":
            client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
        else:
            client = MongoClient(str(mongo_url))
            
        db = client.get_database('sites') #pega o database
        collection = db.sector #pega a collection desejada

        lista_to_insert = [] #lista que amarzenará os novos documentos

        for id_ in lista_com_ids:

            # cria uma nova linha com o id novo
            new_row = {"source": id_}

            # adiciona o novo documento
            lista_to_insert.append(new_row)

        collection.insert_many(lista_to_insert) #atualiza os documentos
    else:
        pass
    return

# ------------------------------------------------------------------------------

#determina a url do site desejado
url = "https://www.thirdsectorcap.org/projects/"

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

# pega o conteúdo da url
driver.get(url)

#tempo para carregar a página inteira
time.sleep(10)

#pega a lista de projetos
lista_de_projetos = acha_lista(1000, "#ngo > div.portifolio-table-nav > div", driver)

#carrega projetos antigos
lista_antigos = transforma_data(sys.argv[1])

#pega os projetos novos
lista_projetos_novos = compara(lista_de_projetos, lista_antigos)

#atualizando a lista de ids backups
atualizaBackUP(lista_projetos_novos, sys.argv[1], sys.argv[2])

#fecha o driver
driver.close()

print(lista_projetos_novos)
sys.stdout.flush()