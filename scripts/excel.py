from openpyxl import load_workbook
import rutas


def pegar_datos_en_excel(afiliado, medicacion_lista, cantidades, cod_troquel, pedido_externo):
    global fila
    print(f"\t\t# INTENTANDO ACCEDER AL EXCEL...")
    excel = load_workbook(rutas.archivo_excel_padre)
    hoja = excel["inicio"]

    #codigo_afiliado = afiliado[0][0] + afiliado[0][1]
    ultima_fila = len(hoja["B"])

    try:
        print(f"\t\t> Se accedio correctamente.")
        for i in range(len(medicacion_lista)):
            hoja[f"A{fila}"].value = " ".join(medicacion_lista[i])
            hoja[f"B{fila}"].value = afiliado.rstrip()
            hoja[f"C{fila}"].value = cod_troquel[i]
            hoja[f"D{fila}"].value = " ".join(cantidades[i])
            hoja[f"E{fila}"].value = pedido_externo

            fila += 1


    except Exception as e:
        print(f"Ha ocurrido una excepcion. Posiblemente hay un error con el EXCEL. {e}")
    # Guardamos y cerramos el excel.
    finally:
        excel.save(ruta_excel)