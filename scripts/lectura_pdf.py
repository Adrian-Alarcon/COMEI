import slate3k
import os
import time


def leer_pdf(ruta_pdf):
    with open(ruta_pdf, "rb") as f:
        datos = slate3k.PDF(f)

    datos_2 = list(map(lambda x: x.replace("\n", " "), datos))
    datos_3 = datos_2[0].split("  ")

    referencia_cod = datos_3.index("CÓDIGO")
    referencia_inicio = referencia_cod + 6
    referencia_fin = referencia_inicio + 4

    ref_cod_af = datos_3.index("Afiliado:")
    cod_af = datos_3[ref_cod_af + 1]

    titulos = datos_3[referencia_cod:referencia_inicio]
    descripciones = datos_3[referencia_inicio:referencia_fin]
    autorizacion = datos_3[2]

    print(datos_3)
    # for dato in datos_3:
    #     print(dato)
    # print(descripciones)

    # return descripciones, autorizacion, cod_af


def armar_descripciones(lista_desc):
    cod_troq_y_desc = lista_desc.pop(0)
    lista_troq_y_des = cod_troq_y_desc.split(" ")
    troquel = lista_troq_y_des.pop(0)
    descripcion = " ".join(lista_troq_y_des)

    lista_desc.insert(0, troquel)
    lista_desc.insert(1, descripcion)


ruta_pdfs = "C:/Users/aalarcon/Desktop/OyP/IMPLEMENTACION CON GITHUB/COMEI/pdfs"

for pdf in os.listdir(ruta_pdfs):

    leer_pdf(ruta_pdfs + "/" + pdf)
    print("")
    # armar_descripciones(datos_pdf)
    #
    # troquel = datos_pdf[0]
    # descripcion_material = datos_pdf[1]
    # cantidad = int(float(datos_pdf[2]))
    #
    # print(f"Codigo de TROQUEL: {troquel}", end=" ")
    # print(f"Descripcion de MATERIAL: {descripcion_material}", end=" ")
    # print(f"CANTIDAD: {cantidad}", end=" ")
    # print(f"NRO DE AUTORIZACION: {autorizacion}", sep=" -- ")
    # print(f"Codigo de AFILIADO: {afiliado}", sep=" -- ")
    # print("")
    # print("")
