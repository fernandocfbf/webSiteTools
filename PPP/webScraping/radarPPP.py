# -*- coding: utf-8 -*-
"""

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

# ----------------------------------------------


def transforma_data(url):
    client = MongoClient(str(url))
    db = client.get_database('sites')
    collection = db.radar_ppp
    lista = list(collection.find())

    resposta = {"source": []}
    for document in lista:
        resposta['source'].append(document['source'])

    return resposta

# ----------------------------------------------

def tentativa(numero_de_tentativas, css_code_selector,driver):
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual <= numero_de_tentativas:
        
        #tenta clicar no botão
        try:
            driver.find_element_by_css_selector(css_code_selector).click()
            break
        
        #caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1
    
    #caso o número de tentativas seja igual ao número limite, não foi possível concluir 
    #a ação
    # if tentativa_atual == numero_de_tentativas:
    #     #print("Número de tentativas excedidas")
        
    # #caso contrário, informa que passou no teste
    # else:
    #     #print("Pass tentativa!")
    
    return

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

def acha_lista_de_links(numero_de_tentativas, css_code_selector, driver):
    conta_contratos=1
    conta_paginas=1
    lista_links = []
    #cria uma lista vazia para dar return
    elementos = None
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual < numero_de_tentativas:
        
        try:
            
            
            while(conta_contratos<=9):

                elementos = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article['+str(conta_contratos)+']/div/header/h2/a')

                link = elementos.get_attribute("href")
                lista_links.append(link)
                conta_contratos+=1
                    
              
            break
        
        #caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1
            
    #caso o número de tentativas seja igual ao número limite, não foi possível concluir 
    #a ação
    # if tentativa_atual == numero_de_tentativas:
    #     print("Número de tentativas excedidas")
    
    # #caso contrário, informa que passou no teste
    # else:
        
    #     print("Pass acha_lista!")
    #     #print(elementos[0].text)
        
    return lista_links

def acha_informacoes(numero_de_tentativas, css_code_selector, driver):
    contador=0
    lista_de_infos=[]
    #cria uma lista vazia para dar return
    elementos = None
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual < numero_de_tentativas:
        #lista = driver.find_elements_by_css_selector(css_code_selector)
        #elementos = lista.find_elements_by_class_name("project")
#            print("deu")
        
        #tenta clicar no botão
       
        try:                                      
            nome =  driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/header/h1')
            nome=nome.text
            for i in range(len(nome)):
                if nome[i]=='(':
                    lista_de_infos.append(nome[: i])
                    localizacao = nome[i+1: len(nome)-1]
                    
            #-----------------------------------------------------------------------------------------------
            
                
            lista_de_infos.append(localizacao)
            
            #-----------------------------------------------------------------------------------------------
            
            p1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/div/p[1]')
            if ":" not in p1.text:
                i=0
                while i<len(p1.text):
                    if p1.text[i]=='p' and p1.text[i+1]=='a' and p1.text[i+2]=='r' and p1.text[i+3]=='a':
                        objeto = p1.text[i+4:]
                        lista_de_infos.append(objeto)
                        break
                        
                    i+=1
            else:
                try:
                    objeto=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/div/blockquote/p')
                except:
                    objeto=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/div/blockquote')
                                                    
                                                    
                lista_de_infos.append(objeto.text)
                
            #-----------------------------------------------------------------------------------------------
                
            if p1.text[0] == E:
                ano_de_inicio = p1.text[9:13]
            else:
                ano_de_inicio = p1.text[17:21]
            lista_de_infos.append(ano_de_inicio)
            
            #-----------------------------------------------------------------------------------------------
                                                    
            texto_todo = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/div')
            texto_todo=texto_todo.text
            
            i=0
            while i<len(texto_todo):
                if texto_todo[i]=='p' and texto_todo[i+1]=='r' and texto_todo[i+2]=='a' and texto_todo[i+3]=='z' and texto_todo[i+4]=='o' and texto_todo[i+6]=='d' and texto_todo[i+7]=='e':
                    inicio=i+9
                    fim=i+9
                    while texto_todo[fim]!=',':
                        fim+=1
                    break
                i+=1
            prazo=texto_todo[inicio:fim+8]
            lista_de_infos.append(prazo)
            
            #-----------------------------------------------------------------------------------------------
            
            if "no valor de" not in texto_todo and "com valor de contrato de" not in texto_todo:
                lista_de_infos.append('--')
            
            elif "no valor de" in texto_todo:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='n' and texto_todo[i+1]=='o' and texto_todo[i+3]=='v' and texto_todo[i+4]=='a' and texto_todo[i+5]=='l' and texto_todo[i+6]=='o' and texto_todo[i+7]=='r' and texto_todo[i+9]=='d' and texto_todo[i+10]=='e':
                        inicio=i+12
                        fim=i+12
                        while texto_todo[fim]!=',':
                            fim+=1

                    i+=1
                valor=texto_todo[inicio:fim+4]
                lista_de_infos.append(valor)
                
            else:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='c' and texto_todo[i+1]=='o' and texto_todo[i+2]=='m' and texto_todo[i+4]=='v' and texto_todo[i+5]=='a' and texto_todo[i+6]=='l' and texto_todo[i+7]=='o' and texto_todo[i+8]=='r' and texto_todo[i+10]=='d':
                        inicio=i+23
                        fim=i+23
                        while texto_todo[fim]!=',':
                            fim+=1

                    i+=1
                valor=texto_todo[inicio:fim+4]
                lista_de_infos.append(valor)
                
                
            #-----------------------------------------------------------------------------------------------
            
            
            if "celebrado entre" not in p1.text:
                lista_de_infos.append('--')
            
            else:
                i=0
                while i<len(p1.text):
                    if p1.text[i]=='c' and p1.text[i+1]=='e' and p1.text[i+2]=='l' and p1.text[i+3]=='e' and p1.text[i+4]=='b' and p1.text[i+5]=='r' and p1.text[i+6]=='a' and p1.text[i+7]=='d' and p1.text[i+8]=='o':
                        inicio=i+18

                    i+=1
                contratada_contratante=p1.text[inicio:]
                lista_de_infos.append(contratada_contratante)  
                
            #-----------------------------------------------------------------------------------------------
            #SETOR
            if "(segmento" in p1.text:
                i=0
                while i<len(p1.text):
                    if p1.text[i]=='(' and p1.text[i+1]=='s' and p1.text[i+2]=='e' and p1.text[i+3]=='g' and p1.text[i+4]=='m' and p1.text[i+5]=='e' and p1.text[i+6]=='n' and p1.text[i+7]=='t' and p1.text[i+8]=='o':
                        inicio=i+10
                        
                        fim=i+10
                        while p1.text[fim]!=')':
                            fim+=1

                    i+=1
               
                setor=p1.text[inicio:fim]
                lista_de_infos.append(setor)
                
            
            elif "do segmento de" in p1.text:
                i=0
                while i<len(p1.text):
                    if p1.text[i]=='s' and p1.text[i+1]=='e' and p1.text[i+2]=='g' and p1.text[i+3]=='m' and p1.text[i+4]=='e' and p1.text[i+5]=='n' and p1.text[i+6]=='t' and p1.text[i+7]=='o' and p1.text[i+9]=='d' and p1.text[i+10]=='e':
                        inicio=i+12
                        fim=i+12
                        conta_espaço=0
                        while conta_espaço<=2:
                            if p1.text[fim]==' ':
                                conta_espaço+=1
                            fim+=1

                    i+=1
                setor=p1.text[inicio:fim+1]
                lista_de_infos.append(setor)
                
            else:
                lista_de_infos.append('--')
                
           #-----------------------------------------------------------------------------------------------
            if "PMI" not in texto_todo:
                lista_de_infos.append('--')
            
            else:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='P' and texto_todo[i+1]=='M' and texto_todo[i+2]=='I':
                        inicio=i+3
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m':
                        inicio_2=inicio+3
                        break
                    inicio+=1
                Data_PMI=texto_todo[inicio_2:inicio_2+10]
                lista_de_infos.append(Data_PMI) 
                
            #-----------------------------------------------------------------------------------------------
            
            if "Consulta Pública" not in texto_todo:
                lista_de_infos.append('--')
            
            else:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='C' and texto_todo[i+1]=='o' and texto_todo[i+2]=='n' and texto_todo[i+3]=='s' and texto_todo[i+4]=='u' and texto_todo[i+5]=='l' and texto_todo[i+6]=='t' and texto_todo[i+7]=='a':
                        inicio=i+16
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m':
                        inicio_2=inicio+3
                        break
                    inicio+=1
                Data_consulta=texto_todo[inicio_2:inicio_2+10]
                lista_de_infos.append(Data_consulta)
                
            #-----------------------------------------------------------------------------------------------
                
            if "Licitação" not in texto_todo or "licitação" not in texto_todo:
                lista_de_infos.append('--')
            
            else:
                i=0
                while i<len(texto_todo):
                    if (texto_todo[i]=='L' or texto_todo[i]=='l') and texto_todo[i+1]=='i' and texto_todo[i+2]=='c' and texto_todo[i+3]=='i' and texto_todo[i+4]=='t' and texto_todo[i+5]=='a' and texto_todo[i+6]=='ç' and texto_todo[i+7]=='ã' and texto_todo[i+8]=='o':
                        inicio=i+16
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m':
                        inicio_2=inicio+3
                        break
                    inicio+=1
                Data_licitacao=texto_todo[inicio_2:inicio_2+10]
                lista_de_infos.append(Data_licitacao)
            
            #-----------------------------------------------------------------------------------------------
           
            i=0
            while i<len(p1.text):
                if (p1.text[i]=='E' or p1.text[i]=='e') and p1.text[i+1]=='m':
                    inicio=i+3
                    break
                i+=1
            Data_ass=p1.text[inicio:inicio+10]
            lista_de_infos.append(Data_ass)
            
            #-----------------------------------------------------------------------------------------------
            
            if "Concessão Patrocinada" not in texto_todo:
                lista_de_infos.append('Concessão Administrativa')
            else:
                lista_de_infos.append('Concessão Patrocinada')
                
            #-----------------------------------------------------------------------------------------------
            if "Concorrência do tipo" not in texto_todo and "Concorrência Nacional do tipo" not in texto_todo and "Concorrência Internacional do tipo" not in texto_todo:
                lista_de_infos.append('--')
                
            elif "Concorrência Nacional do tipo" in texto_todo:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='C' and texto_todo[i+1]=='o' and texto_todo[i+2]=='n' and texto_todo[i+3]=='c' and texto_todo[i+4]=='o' and texto_todo[i+5]=='r' and texto_todo[i+6]=='r' and texto_todo[i+7]=='ê' and texto_todo[i+8]=='n' and texto_todo[i+9]=='c' and texto_todo[i+10]=='i' and texto_todo[i+11]=='a' and texto_todo[i+25]=='t'and texto_todo[i+26]=='i'and texto_todo[i+27]=='p'and texto_todo[i+28]=='o':
                        inicio_v=i+30
                        inicio=i+30
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m' or texto_todo[inicio]=='.':
                        fim=inicio-1
                        break
                    inicio+=1
                Formato_da_concorrencia=texto_todo[inicio_v:fim]
                lista_de_infos.append(Formato_da_concorrencia)
                
            elif "Concorrência Internacional do tipo" in texto_todo:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='C' and texto_todo[i+1]=='o' and texto_todo[i+2]=='n' and texto_todo[i+3]=='c' and texto_todo[i+4]=='o' and texto_todo[i+5]=='r' and texto_todo[i+6]=='r' and texto_todo[i+7]=='ê' and texto_todo[i+8]=='n' and texto_todo[i+9]=='c' and texto_todo[i+10]=='i' and texto_todo[i+11]=='a' and texto_todo[i+30]=='t'and texto_todo[i+31]=='i'and texto_todo[i+32]=='p'and texto_todo[i+33]=='o':
                        inicio_v=i+35
                        inicio=i+35
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m' or texto_todo[inicio]=='.':
                        fim=inicio-1
                        break
                    inicio+=1
                Formato_da_concorrencia=texto_todo[inicio_v:fim]
                lista_de_infos.append(Formato_da_concorrencia)
                
                
                
            else:
                i=0
                while i<len(texto_todo):
                    if texto_todo[i]=='C' and texto_todo[i+1]=='o' and texto_todo[i+2]=='n' and texto_todo[i+3]=='c' and texto_todo[i+4]=='o' and texto_todo[i+5]=='r' and texto_todo[i+6]=='r' and texto_todo[i+7]=='ê' and texto_todo[i+8]=='n' and texto_todo[i+9]=='c' and texto_todo[i+10]=='i' and texto_todo[i+11]=='a' and texto_todo[i+16]=='t'and texto_todo[i+17]=='i'and texto_todo[i+18]=='p'and texto_todo[i+19]=='o':
                        inicio_v=i+21
                        inicio=i+21
                        break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+1]=='m' or texto_todo[inicio]=='.':
                        fim=inicio-1
                        break
                    inicio+=1
                Formato_da_concorrencia=texto_todo[inicio_v:fim]
                lista_de_infos.append(Formato_da_concorrencia)
                
                
            #-----------------------------------------------------------------------------------------------
                
            if "A concessionária vencedora é" not in texto_todo and "A Concessionária vencedora é" not in texto_todo:
                lista_de_infos.append('--')
                
            else:
                i=0
                while i<len(texto_todo):
                    if (texto_todo[i]=='c' or texto_todo[i]=='C') and texto_todo[i+1]=='o' and texto_todo[i+2]=='n' and texto_todo[i+3]=='c' and texto_todo[i+4]=='e' and texto_todo[i+5]=='s' and texto_todo[i+6]=='s' and texto_todo[i+7]=='i' and texto_todo[i+8]=='o' and texto_todo[i+9]=='n' and texto_todo[i+10]=='á' and texto_todo[i+11]=='r' and texto_todo[i+12]=='i' and texto_todo[i+13]=='a' and texto_todo[i+15]=='v'and texto_todo[i+16]=='e'and texto_todo[i+17]=='n'and texto_todo[i+18]=='c'and texto_todo[i+19]=='e'and texto_todo[i+20]=='d'and texto_todo[i+21]=='o'and texto_todo[i+22]=='r'and texto_todo[i+23]=='a':
                        if "A concessionária vencedora é formada pela(s) empresa(s)" in texto_todo or "A Concessionária vencedora é formada pela(s) empresa(s)" in texto_todo:
                            inicio_v=i+54
                            inicio=i+54
                            break
                            
                        elif "A concessionária vencedora é formada pelas empresas" in texto_todo or "A Concessionária vencedora é formada pelas empresas" in texto_todo:
                            inicio_v=i+50
                            inicio=i+50
                            break
                            
                        else:
                            inicio_v=i+47
                            inicio=i+47
                            break

                    i+=1
                while inicio<len(texto_todo):
                    if texto_todo[inicio]=='e' and texto_todo[inicio+2]=='a':
                        fim=inicio-1
                        break
                    inicio+=1
                Integrantes_concessao=texto_todo[inicio_v:fim]
                lista_de_infos.append(Integrantes_concessao)
                
            
             
                
                
            break
        
        #caso não funcione, aumenta a tentativa
        except Exception as e:
            print('except')
            print(e)
            tentativa_atual += 1
            
    #caso o número de tentativas seja igual ao número limite, não foi possível concluir 
    #a ação
    if tentativa_atual == numero_de_tentativas:
        print("Número de tentativas excedidas")
        nome =  driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/main/article/header/h1')
        print("DEU ERRO:", nome.text)
    
    #caso contrário, informa que passou no teste
    else:
        
        print("Pass acha_lista!")
        #print(elementos[0].text)
        
    return lista_de_infos

# ------------------------------------------------------------------

def projetos_antigos(url):
    if str(sys.argv[3]) == "production":
        client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
    else:
        client = MongoClient(str(url))

    db = client.get_database('sites')
    collection = db.radar_ppp
    lista = list(collection.find())

    resposta = []
    for document in lista:
        resposta.append(document)

    return resposta[0]

# ------------------------------------------------------------------

def atualizaBackUP(lista_com_links, url, boolean):

    if str(boolean) == "true" and len(lista_com_links) > 0:
        # if str(sys.argv[3]) == "production":
        #     client = MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/sites"))
    
        # else:
        #     client = MongoClient(str(url))

        # db = client.get_database('sites')  # pega o database
        # collection = db.go_lab  # pega a collection desejada

        # collection.insert_many(lista_com_links)  # atualiza os documentos
        # IRÁ ATUALIZAR O ARQUIVOS
        arq = open("./PPP/webScraping/ultimoLink.txt")
        arq.truncate(0)
        arq.write(lista_com_links[0])
        arq.close()
        print("Text successfully replaced")
    else:
        pass

    return

# ----------------------------------------------
arq = open("./PPP/webScraping/ultimoLink.txt")
ultimo_link = arq.read()
#ultimo_link = projetos_antigos(sys.argv[1])

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

n = 1
links = []

roda = True

while roda == True:
    url = "https://radarppp.com/resumo-de-contratos-de-ppps/page/"+str(n)+"/"
    #cria o webdriver
    #driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

    #pega o conteúdo da url
    driver.get(url)
    
    # driver.find_elements_by_class_name("QvFrame Document_TX2504_224852472")[0].click()

    #tempo para carregar a página inteira
    time.sleep(5)
    
    

    #fecha pop-up
    tentativa(1000, "#ngo > div.ngo-popup > div.got-it", driver)

    lista_de_links = acha_lista_de_links(1000, "#ngo > div.view-content-wrap  > div", driver)

    #print(lista_de_links)
    for elemento in lista_de_links:
        if elemento == ultimo_link:
            roda = False
            break
        links.append(elemento) #(elemento.text)
        
    

    n+=1
    driver.close()

info=0

lista_de_dados=[]

# Atualiza ultimo link

while info<(len(links)):
    url = links[info]

    #cria o webdriver
    driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

    #pega o conteúdo da url
    driver.get(url)
    
    # driver.find_elements_by_class_name("QvFrame Document_TX2504_224852472")[0].click()

    #tempo para carregar a página inteira
    time.sleep(2)
    
    #fecha pop-up
    tentativa(1000, "#ngo > div.ngo-popup > div.got-it", driver)

    dados = acha_informacoes(5, "#ngo > div.parcerias_tb_dados_parceria > div", driver)
    dados.append(url)
  
    lista_de_dados.append(dados) #(elemento.text)
    
    
    #print(info)
    info+=1
    driver.close()

Nome=[]
Localizacao=[]
Objeto=[]
Ano_de_inicio=[]
Duracao=[]
Valor=[]
Contratante_Contratada=[]
Setor=[]
Data_PMI=[]
Data_consulta_publica=[]
Data_licitacao=[]
Data_assinatura_do_contrato=[]
Tipo_de_PPP=[]
Formato_da_concorrencia=[]
Integrantes_concessao=[]
Link=[]


for listas in lista_de_dados:
    Nome.append(listas[0])
    Localizacao.append(listas[1])
    Objeto.append(listas[2])
    Ano_de_inicio.append(listas[3])
    Duracao.append(listas[4])
    Valor.append(listas[5])
    Contratante_Contratada.append(listas[6])
    Setor.append(listas[7])
    Data_PMI.append(listas[8])
    Data_consulta_publica.append(listas[9])
    Data_licitacao.append(listas[10])
    Data_assinatura_do_contrato.append(listas[11])
    Tipo_de_PPP.append(listas[12])
    Formato_da_concorrencia.append(listas[13])
    Integrantes_concessao.append(listas[14])
    Link.append(listas[15])
    
    
    
dicionario = {}
dicionario["Nome"] = Nome
dicionario["Localização"] = Localizacao
dicionario["Objeto"] = Objeto
dicionario["Ano de inicio"] = Ano_de_inicio
dicionario["Duração"] = Duracao
dicionario["Valor"] = Valor
dicionario["Contratante e Contratada"] = Contratante_Contratada
dicionario["Setor"] = Setor
dicionario["Data PMI"] = Data_PMI
dicionario["Data consulta pública"] = Data_consulta_publica
dicionario["Data_licitação"] = Data_licitacao
dicionario["Data assinatura do contrato"] = Data_assinatura_do_contrato
dicionario["Tipo de PPP"] = Tipo_de_PPP
dicionario["Formato da concorrência"] = Formato_da_concorrencia
dicionario["Integrantes concessão"] = Integrantes_concessao
dicionario["Link"] = Link



if len(Link)>0:
    resposta_final = pd.DataFrame(data=dicionario)
else:
    resposta_final = []




# atualiza o mongo Atlas
update = atualizaBackUP(Link, sys.argv[1], sys.argv[2])


sys.stdout.flush()