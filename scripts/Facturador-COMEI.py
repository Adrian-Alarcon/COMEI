import os
from shutil import move
import rutas
from va01_2 import va01_2
from zsd_toma import toma
from tkinter import *
import tkinter as tk
from tkinter import ttk
from shutil import copy
from lectura_pdf import leer_pdfs
from time import sleep
from excel import LecturaDatosExcel


def interfaz():
     root = Tk()
     root.title("FACTURADOR_COMEI")
     root.resizable(0,0)
     root.geometry('300x300+500+50'.format(500, 600))
     miFrame=Frame(root,width=500)
     miFrame.pack()
     miFrame2=Frame(root)
     miFrame2.pack()

     def facturador():
          copy(rutas.archivo_excel_padre, rutas.excel_copia_trabajo)
          sleep(2)
          datos_excel = LecturaDatosExcel(rutas.excel_copia_trabajo, 2)
          datos_excel.abrir_workbook("inicio")

          #---------VARIABLES--------#
          afiliado_anterior = None
          afiliado_actual = None

          l_canales = datos_excel.valores_col("O")
          l_sectores = datos_excel.valores_col("P")
          l_dispones = datos_excel.valores_col("L")
          l_ped_ext = datos_excel.valores_col("E")
          l_id_mat_sap = datos_excel.valores_col("N")
          l_cantidades_va01 = datos_excel.valores_col("D")
          l_afiliados_sap = datos_excel.valores_col("M")
          filas = datos_excel.valores_col("Q")
          # -- listas de datos para cada afiliado
          l_mat_sap_af = []
          l_cant_af = []
          filas_af = [] # filas donde hay que pegar el numero de pedido creado
          
          # --> FACTURACION <--
          for i in range(len(l_afiliados_sap)):
               afiliado_actual = l_afiliados_sap[i]

               if afiliado_actual == afiliado_anterior or afiliado_anterior == None:
                    l_mat_sap_af.append(l_id_mat_sap[i])
                    l_cant_af.append(l_cantidades_va01[i])
                    filas_af.append(filas[i])

               elif afiliado_actual != afiliado_anterior:
                    pedido_v = va01_2(0, l_canales[i-1],
                                        l_sectores[i-1],
                                        l_dispones[i-1],
                                        l_ped_ext[i-1],
                                        l_mat_sap_af, l_cant_af)
                    pedido_t = toma(0, pedido_v, l_dispones[i-1], l_afiliados_sap[i-1], l_canales[i-1])

                    for fila in filas_af:
                         datos_excel.escribir_valores(fila, "R", pedido_t)
                    l_mat_sap_af.clear()
                    l_cant_af.clear()
                    filas_af.clear()
                    l_mat_sap_af.append(l_id_mat_sap[i])
                    l_cant_af.append(l_cantidades_va01[i])
                    filas_af.append(filas[i])

               if i == len(l_afiliados_sap) - 1:
                    pedido_v = va01_2(0, l_canales[i],
                                        l_sectores[i],
                                        l_dispones[i],
                                        l_ped_ext[i],
                                        l_mat_sap_af, l_cant_af)
                    pedido_t = toma(0, pedido_v, l_dispones[i], l_afiliados_sap[i], l_canales[i])

                    for fila in filas_af:
                         datos_excel.escribir_valores(fila, "R", pedido_t)
                    break
               afiliado_anterior = afiliado_actual
          datos_excel.guardar_cerrar_excel(cerrar=True)
          try:
               move(rutas.excel_copia_trabajo, rutas.carpeta_excel_procesados)
          except:
               print("No se pudo mover el archivo excel a la carpeta de Archivos Procesados.")
     
     def lecturaPdfs():
          resultado_lectura = leer_pdfs()
          print(resultado_lectura)

     
     botonPdf = Button(miFrame, text="Leer PDFS", command=lecturaPdfs)
     botonCrear = Button(miFrame, text="Ejecutar", command=facturador)
     botonPdf.grid(row = 10, column = 2, sticky = "e", padx = 10, pady = 10)
     botonCrear.grid(row = 13, column = 2, sticky = "e", padx = 15, pady = 10)

     root.mainloop()

#interfaz()