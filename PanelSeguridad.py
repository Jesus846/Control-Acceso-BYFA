import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import mysql.connector
from tkcalendar import Calendar  

last_data = None
escaner_activo = False
cap = None

def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="BYFA_CONTROL"
    )
    return conn

def insertar_entrada(nombre, area, hora_entrada, fecha_registro, observaciones):
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute(""" 
            INSERT INTO asistencias (Nombre, Area, Hora_Entrada, Hora_Salida, Fecha, Observaciones)
            VALUES (%s, %s, %s, NULL, %s, %s)
        """, (nombre, area, hora_entrada, fecha_registro, observaciones))
        conn.commit()
        print(f"Entrada registrada para {nombre} en el área {area}.")
    except mysql.connector.Error as e:
        print(f"Error insertando datos: {e}")
        messagebox.showerror("Error", "No se pudo registrar la entrada.")
    finally:
        conn.close()

def actualizar_salida(nombre, area, hora_salida):
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute(""" 
            UPDATE asistencias
            SET Hora_Salida = %s
            WHERE Nombre = %s AND Area = %s AND Hora_Salida IS NULL
        """, (hora_salida, nombre, area))
        
        if cursor.rowcount == 0:
            messagebox.showwarning("No encontrado", f"No se encontró un registro de entrada para {nombre} en el área {area}.")
        else:
            conn.commit()
            print(f"Salida registrada para {nombre} en el área {area}.")
    except mysql.connector.Error as e:
        print(f"Error actualizando datos: {e}")
        messagebox.showerror("Error", "No se pudo actualizar la salida.")
    finally:
        conn.close()

def escanear_qr(escanear_salida=False):
    global escaner_activo, last_data, cap
    escaner_activo = True 
    cap = cv2.VideoCapture(0)

    def capturar_frame():
        global last_data, escaner_activo

        if escaner_activo:  
            ret, frame = cap.read()
            if not ret:
                print("No se puede acceder a la cámara.")
                return

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objs = decode(gray_frame)

            for obj in decoded_objs:
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array([(point.x, point.y) for point in points], np.int32)
                    pts = pts.reshape((-1, 1, 2))  
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                qr_data = obj.data.decode("utf-8")

                if qr_data != last_data:
                    print(f"Datos escaneados: {qr_data}")
                    
                    data_parts = qr_data.split(',')
                    if len(data_parts) >= 2:
                        nombre, area = data_parts[0], data_parts[1]
                    else:
                        messagebox.showwarning("Formato inválido", f"El QR escaneado no contiene los datos esperados: {qr_data}")
                        return

                    if escanear_salida:
                        hora_salida = datetime.now().strftime("%H:%M:%S")
                        print(f"Actualizando salida para {nombre} en el área {area} a las {hora_salida}")
                        actualizar_salida(nombre, area, hora_salida)
                    else:
                        hora_entrada = datetime.now().strftime("%H:%M:%S")
                        fecha_registro = datetime.now().strftime("%Y-%m-%d")
                        observaciones = simpledialog.askstring("Observaciones", f"Ingrese observaciones para {nombre}:")
                        insertar_entrada(nombre, area, hora_entrada, fecha_registro, observaciones or "")
                    
                    last_data = qr_data
                    cargar_datos() 

            cv2.imshow("Escanear QR", frame)
            ventana.after(10, capturar_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                detener_escaneo()

    capturar_frame()

def cargar_datos(fecha=None):
    conn = conectar_bd()
    cursor = conn.cursor()
    
   
    if fecha:
        cursor.execute(""" 
            SELECT Nombre, Area, Hora_Entrada, Hora_Salida, Fecha, Observaciones 
            FROM asistencias 
            WHERE Fecha = %s
        """, (fecha,))
    else:
        cursor.execute("SELECT Nombre, Area, Hora_Entrada, Hora_Salida, Fecha, Observaciones FROM asistencias")
    
    registros = cursor.fetchall()

    for row in tree.get_children():
        tree.delete(row)

    for registro in registros:
        tree.insert("", tk.END, values=registro)

    conn.close()

def detener_escaneo():
    global escaner_activo, cap
    escaner_activo = False  
    if cap is not None:
        cap.release()  
    cv2.destroyAllWindows()

def iniciar_escaneo():
    escanear_qr(escanear_salida=False)

def iniciar_escaneo_salida():
    escanear_qr(escanear_salida=True)

def filtrar_datos():
    fecha = cal.get_date()  
    cargar_datos(fecha)  

def abrir_panel_visitas():
    ventana.destroy()  
    import PanelVisitas  
    PanelVisitas.main()

def main():
    global ventana, tree, cal
    ventana = tk.Tk()
    ventana.title("Registro de Accesos")
    
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    ventana.geometry(f"{screen_width}x{screen_height}")

    
    ventana.grid_rowconfigure(3, weight=1)  
    ventana.grid_columnconfigure(0, weight=1)  
    ventana.grid_columnconfigure(1, weight=1)  
    ventana.grid_columnconfigure(2, weight=1)  

    label_titulo = tk.Label(ventana, text="Panel de Registro de Accesos", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_titulo.grid(row=0, column=0, columnspan=3, pady=(20, 30), sticky="n")

    btn_escanear = tk.Button(ventana, text="Escanear Entrada", command=iniciar_escaneo, width=15)
    btn_escanear.grid(row=1, column=0, padx=5, pady=10)

    btn_escanear_salida = tk.Button(ventana, text="Escanear Salida", command=iniciar_escaneo_salida, width=15)
    btn_escanear_salida.grid(row=1, column=1, padx=5, pady=10)

    btn_detener = tk.Button(ventana, text="Detener Escaneo", command=detener_escaneo, width=15)
    btn_detener.grid(row=1, column=2, padx=5, pady=10)

    btn_visitas = tk.Button(ventana, text="Abrir Panel de Visitas", command=abrir_panel_visitas, width=15)
    btn_visitas.grid(row=2, column=0, padx=5, pady=10)

    btn_cerrar_sesion = tk.Button(ventana, text="Cerrar Sesión", command=ventana.destroy, width=15)
    btn_cerrar_sesion.grid(row=2, column=1, padx=5, pady=10)

   
    frame = tk.Frame(ventana)
    frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  

 
    frame.grid_rowconfigure(1, weight=1)  
    frame.grid_columnconfigure(0, weight=1)  
    frame.grid_columnconfigure(1, weight=1) 

   
    cal = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.grid(row=0, column=0, padx=5, pady=(0, 5))  

    btn_filtrar = tk.Button(frame, text="Filtrar por Fecha", command=filtrar_datos, width=15)
    btn_filtrar.grid(row=0, column=1, padx=5, pady=0) 
    tree = ttk.Treeview(frame, columns=("Nombre", "Área", "Hora de Entrada", "Hora de Salida", "Fecha de Registro", "Observaciones"), show="headings", height=10)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Hora de Entrada", text="Hora de Entrada")
    tree.heading("Hora de Salida", text="Hora de Salida")
    tree.heading("Fecha de Registro", text="Fecha de Registro")
    tree.heading("Observaciones", text="Observaciones")

   
    tree.column("Nombre", width=150)
    tree.column("Área", width=150)
    tree.column("Hora de Entrada", width=150)
    tree.column("Hora de Salida", width=150)
    tree.column("Fecha de Registro", width=150)
    tree.column("Observaciones", width=200)

    tree.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")  

  
    cargar_datos()

    ventana.mainloop()

if __name__ == "__main__":
    main()
