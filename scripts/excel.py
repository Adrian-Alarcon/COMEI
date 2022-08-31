from openpyxl import load_workbook
import rutas
from shutil import copy
from time import sleep
import json

class LecturaDatosExcel:
    def __init__(self, ruta_excel, inicio_filas):
        self.ruta_excel = ruta_excel
        self.inicio_filas = inicio_filas
        self.excel = None
        self.cant_filas = 0
        self.__wb = None

    def abrir_workbook(self, nombre_hoja):
        try:
            self.excel = load_workbook(self.ruta_excel, data_only=True)
            self.__wb = self.excel[f"{nombre_hoja}"]
        except FileNotFoundError:
            return "Error al intentar abrir el archivo pasado como parametro."

    def max_filas(self, col: str):
        max_filas = self.inicio_filas
        if self.__wb != None:
            while self.__wb[f"{col}{max_filas}"].value != None:
                max_filas += 1
            return max_filas
        else:
            return "WB Vacio", self.__wb

    def valores_col(self, *args):
        """args son las columnas de las que necesitamos sus valores"""
        valores = {}
        cant_max_f = self.max_filas("B")
        for col in args:
            if len(args) == 1:
                l_valores = [self.__wb[f"{col}{i}"].value for i in range(self.inicio_filas, cant_max_f) if self.__wb[f"F{i}"].value != "SI"]
                return l_valores
            elif len(args) > 1:
                l_valores = [self.__wb[f"{col}{i}"].value for i in range(self.inicio_filas, cant_max_f) if self.__wb[f"F{i}"].value != "SI"]
                valores[col] = l_valores
                return valores

    def escribir_valores(self, fila, columna, valor):
        self.__wb[f"{columna}{fila}"].value = valor
        self.guardar_cerrar_excel(self.ruta_excel)

    def guardar_cerrar_excel(self, cerrar=False):
        if self.excel != None or self.__wb != None:
            try:
                if cerrar:
                    self.excel.save(self.ruta_excel)
                    self.excel.close()
                else:
                    self.excel.save(self.ruta_excel)
                return True
            except Exception as e:
                print(f"Error al intentar cerrar el excel: {e}")
        else:
            print("No se Pudo cerrar un archivo que no fue abierto.")
            return


