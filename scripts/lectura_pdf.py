import slate3k
import os
import time


def leer_pdf(ruta_pdf):
    """Esta funcion se encarga de leer el pdf y devolver una nueva lista"""
    with open(ruta_pdf, "rb") as f:
        datos = slate3k.PDF(f)
    datos_2 = list(map(lambda x: x.replace("\n", " "), datos))
    datos_3 = datos_2[0].split("  ")
    afiliado = datos_3[datos_3.index("Afiliado:") + 1]
    nro_autorizacion = datos_3[datos_3.index("Autorización Número:") + 1]
    return datos_3, afiliado, nro_autorizacion


# armar y ordenar en una lista nueva los datos de cada pdf
def ordenar_datos():
    nueva_lista = []
    while lista_filtrada_2 != []:
        nuevo_elem = ""
        if lista_filtrada_2[0].isnumeric():
            nuevo_elem += lista_filtrada_2.pop(0)
            nuevo_elem += f" {lista_filtrada_2[0]}"
            lista_filtrada_2.pop(0)
            nueva_lista.append(nuevo_elem)
        else:
            nueva_lista.append(lista_filtrada_2.pop(0))
    return nueva_lista


# De la lista ordenada, se separa el nro de troquel, cantidad y descripcion del material
def separa_troquel_descr(cadena):
    separacion = cadena.split(" ", 1)
    troquel = separacion[0]
    descripcion = separacion[1]
    return troquel, descripcion



# --- PROGRAMA PRINCIPAL --- #
MODELO_TITULOS = ['CÓDIGO', 'DESCRIPCION', 'CANTIDAD', '% COB.', 'ADM', 'MED']
ruta_pdfs = "C:/Users/aalarcon/Desktop/OyP/IMPLEMENTACION CON GITHUB/COMEI/pdfs"


for pdf in os.listdir(ruta_pdfs):
    # lista que viene con todos los datos del PDF
    lista_datos, afiliado, autorizacion = leer_pdf(f"{ruta_pdfs}/{pdf}")

    # lista filtrando los elementos a la derecha de la palabra CÓDIGO
    lista_filtrada = list(filter(lambda x: lista_datos.index(x) >= lista_datos.index(MODELO_TITULOS[0]), lista_datos))

    # armamos otra lista para quedarnos solamente con los datos que nos interesan
    lista_filtrada_2 = list(filter(lambda x: lista_filtrada.index(x) < lista_filtrada.index("AUTORIZADA AUTORIZADA"), lista_filtrada))[6:]

    # Aca la lista ya esta normalizadas y uniforme para poder operar y extraer cod troque + nombre medicacion + cantidades
    nueva_lista = ordenar_datos()
    for d in range(len(nueva_lista)//3):
        marcador = len(nueva_lista)//3
        descripciones_y_troquel = nueva_lista[d]
        troquel, nombre_medicacion = separa_troquel_descr(descripciones_y_troquel)
        cantidades = nueva_lista[marcador + d]
        print(f"AFILIADO: {afiliado} | Nro TROQUEL: {troquel} | NOMBRE MEDICACION: {nombre_medicacion} | CANTIDAD: {int(float(cantidades))}")
    print("----------------------------------------------------")

        # Aca llamar a una funcion que se encargue de cargar todos los datos en un excel