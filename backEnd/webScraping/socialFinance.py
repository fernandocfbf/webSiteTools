# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 19:58:37 2020

@author: Fernando
"""
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os

#determina a url do site desejado
url = "https://sibdatabase.socialfinance.org.uk/"

#cria o webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

#pega o conteúdo da url
driver.get(url)

#tempo para carregar a página inteira
time.sleep(10)

#------------------------------------------------------------------------------
def acha_lista(numero_de_tentativas, css_code_selector):
    
    #cria uma lista vazia para preencher com os elementos
    elementos = []
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual < numero_de_tentativas:

        try:
            
            #tenta encontrar a lista de elementos
            elementos = driver.find_elements_by_class_name("project")
            break
        
        #caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1
            
    #caso o número de tentativas seja igual ao número limite, 
    #não foi possível concluir a ação
    if tentativa_atual == numero_de_tentativas:
        pass
    
    #caso contrário, informa que passou no teste
    else:
        pass
        
    return elementos

#------------------------------------------------------------------------------
def encontra_novos(lista_de_elementos, inseridos):
    
    #cria uma lista vazia de resposta
    lista_novos = list()
    
    for elemento in lista_de_elementos:
        
        if elemento.get_attribute("id") not in inseridos:
            lista_novos.append(elemento.get_attribute("id"))
            
    return lista_novos

#------------------------------------------------------------------------------
def le_excel_social_finance(excel):
    
    #cria uma lista vazia para preencher com os projetos já inseridos
    lista = list()
    
    #cria um dataframe com o arquivo excel
    df = pd.read_excel(excel, engine='openpyxl')
    
    #adiciona todas as linhas na lista de elementos
    df['informacoes'].apply(lambda x: lista.append(x))
    
    return lista

#------------------------------------------------------------------------------
def separa_id(lista_project_index):
    
    #lista com os indices de resposta
    lista_index = list()
    
    #percorre a lista de projetos com o indice
    for project in lista_project_index:
        
        indice = 0
        #looping infinito até encontrar o id
        while indice < len(project):
            
            #se encontrar index_...
            if project[indice:indice+6] == "index_":
                
                #pega o indice e adiciona na lista final
                id_projeto = project[indice+6:len(project)]
                
                lista_index.append(id_projeto)
                
                #para de percorre o texto
                break
            
            #caso não encontre o id do projeto...
            else:
                #adiciona um no indice para continuar
                indice += 1
    
    return lista_index
  
#------------------------------------------------------------------------------ 
def lista_links(ids_projetos):
    
    #lista para resposta
    lista_links = list()
    
    for id_projeto in ids_projetos:
        
        lista_links.append("https://sibdatabase.socialfinance.org.uk/?project_id={0}".format(id_projeto))
        
    return lista_links
    
#------------------------------------------------------------------------------  
def atualizaBackUP(lista_com_ids, path_name):
    
    #lê o arquivo excel
    df = pd.read_excel(path_name, engine='openpyxl')
    
    for id_ in lista_com_ids:
        
        #cria uma nova linha com o id novo
        new_row = {"informacoes":id_}
        
        #escreve a linha no excel
        df = df.append(new_row, ignore_index=True)
    
    df.to_excel(path_name, engine='openpyxl', index=False)
    return 

#------------------------------------------------------------------------------

path = os.path.dirname(__file__) + "/Backup/socialFinance.xlsx"

#cria a lista com projetos já inseridos
lista_projetos_inseridos = le_excel_social_finance(path)

#encontra a lista de projetos com os respectivos códigos
lista_de_projetos = acha_lista(1000, "#ngo > div.project-list.clearfix > div")
                   
#cria lista de novos elementos
lista_de_projetos_novos = encontra_novos(lista_de_projetos, lista_projetos_inseridos)

#cria lista somente com os ids
lista_ids = separa_id(lista_de_projetos_novos)

#cria uma lista com os links dos projetos novos
lista_links_novos = lista_links(lista_ids)

#atualizando a lista de ids backups
atualizaBackUP(lista_de_projetos_novos, path)

print(lista_links_novos)
sys.stdout.flush()










