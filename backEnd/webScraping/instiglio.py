import pandas as pd
from selenium import webdriver
import time
import sys


##----------------------------------------------
def retornaListaLinks(elementos):

    #lista de reposta para return
    resposta = []

    for elemento in elementos:

        #pega o link de cada elemento encontrado
        link = elemento.get_attribute("href")

        #adiciona o link na lista de reposta
        resposta.append(link)

    return resposta

##----------------------------------------------
def pegaListaAntigos(arquivo_excel):

    #cria lista de resposta para return
    resposta = []

    #le o arquivo excel com o backup dos links já adicionados
    df = pd.read_excel(arquivo_excel)

    #adiciona todos os links antigos na lista de resposta
    df["informacoes"].apply(lambda x: resposta.append(x))

    return resposta

##----------------------------------------------
def comparaListas(lista1, lista2):

    #cria lista de resposta para return
    resposta = []

    #vamos comparar cada elemento das duas lista
    for elemento in lista1:
        
        #se o elemento da lista1 não estiver na lista2...
        if elemento not in lista2:

            #adiciona o elemento novo na lista de resposta
            resposta.append(elemento)
        
        #se o elemento já estiver na outra lista, o link é antigo
        else:
            pass
    
    return resposta

##----------------------------------------------  
def atualizaBackUP(lista_com_links):
    
    #lê o arquivo excel
    df = pd.read_excel("./Backup/instiglio.xlsx")
    
    for id_ in lista_com_links:
        
        #cria uma nova linha com o id novo
        new_row = {"informacoes":id_}
        
        #escreve a linha no excel
        df = df.append(new_row, ignore_index=True)
    
    df.to_excel("./Backup/instiglio.xlsx", index=False)
    
    return 

##----------------------------------------------  
            
#determina a url do site desejado
url = "https://www.instiglio.org/en/projects/"

#cria o webdriver
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

#pega o conteúdo da url
driver.get(url)

#tempo para carregar a página inteira
time.sleep(2)

#encontra a lista de elementos
elementos = driver.find_elements_by_css_selector(".wpb_wrapper [href]")

#cria lista de links encontrados
lista_links = retornaListaLinks(elementos)

#cria a lista de antigos:
lista_antigos = pegaListaAntigos("./Backup/instiglio.xlsx")

#cria a lista com os links novos
lista_novos_links = comparaListas(lista_links, lista_antigos)

#atualiza o arquivo de backup
atualizaBackUP(lista_novos_links)

print(lista_novos_links)
sys.stdout.flush()


