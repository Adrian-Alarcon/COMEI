import os
from getpass import getuser
import datetime

# VARIABLES
usuario = getuser()
ahora = datetime.datetime.now()
fecha_actual = ahora.strftime("%d-%m-%Y - %H:%M:%S")
print(fecha_actual)

# --> obtenemos la ruta del directorio actual.
directorio_raiz = f"C:/Users/{usuario}/Documents/Clientes Carga Automatica/COMEI"

# --> Armamos la ruta del directorio de archivos.
directorio_archivos = directorio_raiz + "/" + "archivos"

# --> Armamos la ruta del Excel.
excel_copia_trabajo = directorio_archivos + "/" + f"{fecha_actual} - ComeiPadronTrabajoSap.xlsx"
archivo_excel_padre = directorio_archivos + "/" + "ComeiPadre.xlsx"

# --> Ruta carpeta de pdfs.
carpeta_pdfs = os.path.join(directorio_raiz, "pdfs")
carpeta_pdf_procesados = os.path.join(directorio_raiz, "pdf_procesados")
carpeta_pdf_no_procesados = os.path.join(directorio_raiz, "pdf_procesados")



