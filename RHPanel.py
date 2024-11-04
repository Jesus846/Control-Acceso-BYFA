import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime
import pandas as pd
import os
import QRAsistencias
import QRVisitas


def obtener_datos_tabla(fecha=None):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="BYFA_CONTROL"  
        )
        cursor = conexion.cursor()
        if fecha:
            query = "SELECT Nombre, Area, Hora_Entrada, Hora_Salida, Fecha, Observaciones FROM asistencias WHERE Fecha = %s"
            cursor.execute(query, (fecha,))
        else:
            cursor.execute("SELECT Nombre, Area, Hora_Entrada, Hora_Salida, Fecha, Observaciones FROM asistencias")
        
        datos = cursor.fetchall()
        conexion.close()
        return datos
    except mysql.connector.Error as err:
        print("Error al conectar con la base de datos:", err)
        return []

def filtrar_por_fecha():
    fecha_seleccionada = date_entry.get_date()
    fecha_formateada = fecha_seleccionada.strftime("%Y-%m-%d")

    for item in tree.get_children():
        tree.delete(item)
    
    datos = obtener_datos_tabla(fecha_formateada)
    for fila in datos:
        tree.insert("", "end", values=fila)

def exportar_excel(fecha=None):
    datos_tabla = []
    for row_id in tree.get_children():
        row = tree.item(row_id)['values']
        datos_tabla.append(row)

    columnas = ["Nombre", "Área", "Hora Entrada", "Hora Salida", "Fecha", "Observaciones"]
    df = pd.DataFrame(datos_tabla, columns=columnas)
    
    if fecha:
        fecha_formateada = fecha.strftime("%Y-%m-%d")
        nombre_archivo = f"reporte_accesos_{fecha_formateada}.xlsx"
    else:
        nombre_archivo = "reporte_accesos.xlsx"
    
    carpeta_reportes = "ReportesRH"
    if not os.path.exists(carpeta_reportes):
        os.makedirs(carpeta_reportes)

    ruta_archivo = os.path.join(carpeta_reportes, nombre_archivo)
    df.to_excel(ruta_archivo, index=False)

    messagebox.showinfo("Éxito", f"Reporte exportado exitosamente como '{ruta_archivo}'")

def abrir_QR():
    QRAsistencias.abrir_ventana_qr(root)

def abrir_QR_visitas():
    QRVisitas.abrir_ventana_qr(root)

def main():
    global root, tree, date_entry
    root = tk.Tk()
    root.title("Registro de Accesos")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    btn_abrir_qr = tk.Button(root, text="Generador de QR Asistencia", command=abrir_QR)
    btn_abrir_qr.pack(pady=20)

    btn_abrir_qr_visitas = tk.Button(root, text="Generador de QR Visitas", command=abrir_QR_visitas)
    btn_abrir_qr_visitas.pack(pady=20)

    btn_volver = tk.Button(root, text="Cerrar Sesión", command=root.destroy)
    btn_volver.pack(pady=20)

    tk.Label(root, text="Filtrar por Fecha:", font=("Arial", 12)).pack(pady=5)
    date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
    date_entry.pack(pady=5)

    btn_filtrar = tk.Button(root, text="Filtrar", command=filtrar_por_fecha, font=("Arial", 12), bg="#FFC107")
    btn_filtrar.pack(pady=10)

    btn_exportar = tk.Button(root, text="Exportar a Excel", command=lambda: exportar_excel(date_entry.get_date()), font=("Arial", 12), bg="#8E44AD", fg="white")
    btn_exportar.pack(pady=10)

    tree = ttk.Treeview(root, columns=("Nombre", "Área", "Hora_Entrada", "Hora_Salida", "Fecha", "Observaciones"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Hora_Entrada", text="Hora Entrada")
    tree.heading("Hora_Salida", text="Hora Salida")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Observaciones", text="Observaciones")

    for col in ("Nombre", "Área", "Hora_Entrada", "Hora_Salida", "Fecha", "Observaciones"):
        tree.column(col, width=250, anchor="center")

    datos = obtener_datos_tabla()
    for fila in datos:
        tree.insert("", "end", values=fila)

    tree.pack(pady=20, fill="x", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
