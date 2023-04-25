import slate3k
import os
import rutas
import shutil
import re
from openpyxl import load_workbook

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
def ordenar_datos(lista_filtrada_2):
    nueva_lista = []
    while lista_filtrada_2 != []:
        nuevo_elem = ""
        if lista_filtrada_2[0] not in MODELO_TITULOS and not re.findall('accesorios',lista_filtrada_2[0]) != []:
            if lista_filtrada_2[0].isnumeric(): #preguntar si es que la palabra de la posicion esta en MODELO TITULOS o si tiene la palabra autorizacion dentro
                nuevo_elem += lista_filtrada_2.pop(0)
                nuevo_elem += f" {lista_filtrada_2[0]}"
                lista_filtrada_2.pop(0)
                nueva_lista.append(nuevo_elem)
            else:
                nueva_lista.append(lista_filtrada_2.pop(0))
        else:
            lista_filtrada_2.pop(0)
    return nueva_lista

def reordenar_datos(lista_filtrada_2):
    nueva_lista = []
    while lista_filtrada_2 != []:
        nuevo_elem = ""
        if lista_filtrada_2[0].isnumeric():
            nuevo_elem += lista_filtrada_2.pop(0)
            nuevo_elem += f" {lista_filtrada_2[0]}"
            lista_filtrada_2.pop(0)
            nueva_lista.append(nuevo_elem)
        elif lista_filtrada_2[0] in MODELO_TITULOS:
            lista_filtrada_2.pop(0)    
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
MODELO_TITULOS = ['CÓDIGO', 'DESCRIPCION', 'CANTIDAD', '% COB.', 'ADM', 'MED','Observaciones:']
ruta_pdfs = rutas.carpeta_pdfs

# Variable global para el Excel
def leer_pdfs():
    
    fila = 2
    excel = load_workbook(rutas.archivo_excel_padre)
    hoja = excel["inicio"]
    listaCambiada = False
    cant = hoja[f"Q"]
    #print("Cantidad de filas ya procesadas: ",cant)

    #Ver con Adri de un control dentro del excel, antes de iniciar toda la carga de la informacion leida por el bot
    #Que la columna Q la borre y deje vacia, asi la vamos completando a medida que se completan las filas

    for pdf in os.listdir(ruta_pdfs):
        try:
            # lista que viene con todos los datos del PDF
            lista_datos, afiliado, autorizacion = leer_pdf(f"{ruta_pdfs}/{pdf}")

            # lista filtrando los elementos a la derecha de la palabra CÓDIGO
            lista_filtrada = list(filter(lambda x: lista_datos.index(x) >= lista_datos.index(MODELO_TITULOS[0]), lista_datos))

            # armamos otra lista para quedarnos solamente con los datos que nos interesan
            # en caso de tener un orden de datos diferentes, se ubica por la variable fija "CANTIDAD"
            if lista_filtrada[2] == "CANTIDAD":
                lista_filtrada_2 = list(filter(lambda x: lista_filtrada.index(x) < lista_filtrada.index("AUTORIZADA AUTORIZADA"), lista_filtrada))[6:]
                nueva_lista = ordenar_datos(lista_filtrada_2)
            else:
                lista_filtrada_2 = list(filter(lambda x: lista_filtrada.index(x) < lista_filtrada.index("AUTORIZADA AUTORIZADA"), lista_filtrada))[2:]
                if lista_filtrada_2[1] == "Observaciones:" or lista_filtrada_2[1] == "Fecha de Vencimiento:":
                    lista_aux = []
                    lista_aux.append(lista_filtrada_2[0])
                    lista_aux += list(filter(lambda x: lista_filtrada_2.index(x) > lista_filtrada_2.index("Provincia:") and lista_filtrada_2.index(x) > lista_filtrada_2.index("Provincia:"), lista_filtrada_2))
                    listaCambiada = True
                if lista_filtrada_2[1] != "Edad:" and not listaCambiada:
                    nueva_lista = reordenar_datos(lista_filtrada_2)
                else:
                    lista_aux_2 = []
                    lista_aux_2.append(lista_filtrada_2[0])
                    lista_aux_2 += list(filter(lambda x: lista_filtrada_2.index(x) > lista_filtrada_2.index("CANTIDAD"), lista_filtrada_2))
                    
                    nueva_lista = reordenar_datos(lista_aux_2)
            
            # Al final se crea una nueva lista donde
            # ya esta normalizada y uniforme para poder operar y extraer cod troque + nombre medicacion + cantidades
            
            for d in range(len(nueva_lista)//3):
                marcador = len(nueva_lista)//3
                descripciones_y_troquel = nueva_lista[d]
                troquel, nombre_medicacion = separa_troquel_descr(descripciones_y_troquel)
                cantidades = nueva_lista[marcador + d]
                cantidades = int(float(cantidades))

                ### -- PEGADO DE DATOS EN EL EXCEL -- ###
                if str(cantidades).isnumeric() and troquel.isnumeric():
                    hoja[f"A{fila}"].value = nombre_medicacion
                    hoja[f"B{fila}"].value = afiliado.rstrip()
                    hoja[f"C{fila}"].value = troquel.rstrip()
                    hoja[f"D{fila}"].value = cantidades
                    hoja[f"E{fila}"].value = autorizacion  # Pedido Externo
                    #hoja[f"Q{fila}"].value = fila #Agregar el numero de fila a la columna Q
                    #[f"P{fila}"].value = convenio
                    fila += 1

                print(f"AFILIADO: {afiliado} | Nro TROQUEL: {troquel} | NOMBRE MEDICACION: {nombre_medicacion} | CANTIDAD: {int(float(cantidades))}")
            print("----------------------------------------------------\n")
            shutil.move(ruta_pdfs + "/" + pdf, rutas.carpeta_pdf_procesados + "/" + pdf)
            excel.save(rutas.archivo_excel_padre)
        except Exception as e:
            print("---------------------------------------------------------------------------------------")
            print(f"********* El PDF {pdf} NO PUDO SER LEIDO Y CARGADO O EL EXCEL NO ES VALIDO ***********")
            print("---------------------------------------------------------------------------------------")
            print(e)
            shutil.move(ruta_pdfs + "/" + pdf, rutas.carpeta_pdf_no_procesados + "/" + pdf)
            continue
        finally:
            excel.save(rutas.archivo_excel_padre)


leer_pdfs()