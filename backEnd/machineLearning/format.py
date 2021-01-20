import pandas as pd

def xlsx_to_json():

    df = pd.read_excel("input_train.xlsx")

    lista_manchetes = []
    lista_relevancia = []

    for i in df.index:

        lista_manchetes.append(df["Manchete"][i])
        lista_relevancia.append(df["Relevância"][i])
    
    data = {
        "Manchete":lista_manchetes,
        "Relevância":lista_relevancia
    }

    return data

d = xlsx_to_json()

print(d)
    



