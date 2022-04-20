import slate3k
import os
import time


def leer_pdf(ruta_pdf):
    """Esta funcion se encarga de leer el pdf y devolver una nueva lista"""
    with open(ruta_pdf, "rb") as f:
        datos = slate3k.PDF(f)
    datos_2 = list(map(lambda x: x.replace("\n", " "), datos))
    datos_3 = datos_2[0].split("  ")
    return datos_3      #devuelvo una lista con toda la info del pdf


# armar los datos de cada pdf
def armar_datos(lista_filtrada):
    datos = lista_filtrada[6:]
    print(datos)
    """
    for i in range(len(datos)):
        print(datos[i].split(" ", 1))
    """


# --- PROGRAMA PRINCIPAL --- #
MODELO_TITULOS = ['CÓDIGO', 'DESCRIPCION', 'CANTIDAD', '% COB.', 'ADM', 'MED']
ruta_pdfs = "C:/Users/aalarcon/Desktop/OyP/IMPLEMENTACION CON GITHUB/COMEI/pdfs"


for pdf in os.listdir(ruta_pdfs):
    # lista que viene con todos los datos del PDF
    lista_datos = leer_pdf(f"{ruta_pdfs}/{pdf}")

    # armamos una nueva lista filtrando los elementos a la derecha de la palabrea CÓDIGO
    lista_filtrada = list(filter(lambda x: lista_datos.index(x) >= lista_datos.index(MODELO_TITULOS[0]), lista_datos))

    # armamos otra lista para quedarnos solamente con los datos que nos interesan
    lista_filtrada_2 = list(filter(lambda x: lista_filtrada.index(x) < lista_filtrada.index("AUTORIZADA AUTORIZADA"), lista_filtrada))
    armar_datos(lista_filtrada_2)
    print()