import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, simpledialog
from datetime import datetime
from PIL import Image, ImageTk
import mysql.connector


def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="BYFA_CONTROL"
    )
    return conn


def insertar_visita(tarjeta, usuario, nombre, areas, observaciones, hora_entrada, fecha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        for area in areas:
            cursor.execute(""" 
                INSERT INTO visitas (Numero_de_tarjeta, Usuario_General, Nombre, Area, Observaciones, Hora_Entrada, Hora_Salida, Fecha)
                VALUES (%s, %s, %s, %s, %s, %s, NULL, %s)
            """, (tarjeta, usuario, nombre, area, observaciones, hora_entrada, fecha))  
        conn.commit()
        print(f"Visita registrada para {nombre} en las áreas {', '.join(areas)}.")
    except mysql.connector.Error as e:
        print(f"Error insertando datos: {e}")
        messagebox.showerror("Error", "No se pudo registrar la visita.")
    finally:
        conn.close()


def cargar_datos():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT Numero_de_tarjeta, Usuario_General, Nombre, Area, Observaciones, Hora_Entrada, Hora_Salida, Fecha FROM visitas")
    registros = cursor.fetchall()

    for row in tree.get_children():
        tree.delete(row)


    for registro in registros:
        tree.insert("", tk.END, values=registro)

    conn.close()


def escanear_qr():
    global cap, lbl_video, cam_window
    cam_window = Toplevel(ventana)
    cam_window.title("Escaneo de QR")
    cam_window.geometry("600x500")
    lbl_video = tk.Label(cam_window)
    lbl_video.pack()

    btn_detener = tk.Button(cam_window, text="Detener escaneo", command=detener_escaneo)
    btn_detener.pack(pady=10)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "No se puede acceder a la cámara.")
        cam_window.destroy()
        return

    mostrar_video()

def mostrar_video():
    global cap, lbl_video

    ret, frame = cap.read()
    if not ret:
        lbl_video.after(10, mostrar_video)
        return

  
    decoded_objs = decode(frame)
    for obj in decoded_objs:
        qr_data = obj.data.decode("utf-8")
        print(f"Datos escaneados: {qr_data}")

        data_parts = qr_data.split(',')
        if len(data_parts) >= 2:
            tarjeta = data_parts[0] 
            usuario = data_parts[1]   

           
            nombre = simpledialog.askstring("Nombre del Visitante", "Ingrese el nombre del visitante:")
            if nombre is None or nombre.strip() == "":
                messagebox.showwarning("Nombre requerido", "El nombre del visitante es obligatorio.")
                detener_escaneo()
                return
            
        
            observaciones = simpledialog.askstring("Observaciones", "Ingrese observaciones sobre la visita:")
            if observaciones is None:
                observaciones = "" 
            
        else:
            messagebox.showwarning("Formato inválido", f"El QR escaneado no contiene los datos esperados: {qr_data}")
            detener_escaneo()
            return
        
        
        hora_entrada = datetime.now().strftime("%H:%M:%S")  
        fecha = datetime.now().strftime("%Y-%m-%d")  
        print(f"Hora de entrada: {hora_entrada}, Fecha: {fecha}") 

        
        areas = [area for area, var in area_vars.items() if var.get()]
        if areas:
            insertar_visita(tarjeta, usuario, nombre, areas, observaciones, hora_entrada, fecha)
            cargar_datos()
        else:
            messagebox.showwarning("Selección de área", "Seleccione al menos un área para registrar la visita.")
        
        detener_escaneo()
        return

    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    lbl_video.configure(image=img)
    lbl_video.image = img

    lbl_video.after(10, mostrar_video)


def detener_escaneo():
    global cap
    if cap.isOpened():
        cap.release()
    cam_window.destroy()

def abrir_panel_seguridad():
    ventana.destroy()  

    import PanelSeguridad  
    PanelSeguridad.main()

def main():
    global ventana, tree, area_vars
    ventana = tk.Tk()
    ventana.title("Registro de Visitas")

    label_titulo = tk.Label(ventana, text="Panel de Registro de Visitas", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_titulo.pack(pady=20)

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    ventana.geometry(f"{screen_width}x{screen_height}")

 
    btn_escanear = tk.Button(ventana, text="Escanear QR para Visita", command=escanear_qr)
    btn_escanear.pack(pady=10)
    
    area_frame = tk.Frame(ventana)
    area_frame.pack(pady=10)
    tk.Label(area_frame, text="Seleccione el área de visita:").pack(anchor='w')
    
    areas_disponibles = ["Recepción", "Producción", "Almacén", "Oficinas"]
    area_vars = {area: tk.BooleanVar() for area in areas_disponibles}

    for area, var in area_vars.items():
        chk = tk.Checkbutton(area_frame, text=area, variable=var)
        chk.pack(anchor='w')

   
    tree = ttk.Treeview(ventana, columns=("Numero_de_tarjeta", "Usuario", "Nombre", "Área", "Observaciones", "Hora de Entrada", "Hora de Salida", "Fecha"), show="headings", height=10)
    tree.heading("Numero_de_tarjeta", text="Número de Tarjeta")
    tree.heading("Usuario", text="Usuario General")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Observaciones", text="Observaciones")
    tree.heading("Hora de Entrada", text="Hora de Entrada")
    tree.heading("Hora de Salida", text="Hora de Salida")
    tree.heading("Fecha", text="Fecha")
    tree.pack(pady=20)

    btn_regresar = tk.Button(ventana, text="Regresar", command=abrir_panel_seguridad, width=20)
    btn_regresar.pack(pady=20)

    cargar_datos() 
    ventana.mainloop()

if __name__ == "__main__":
    main()

