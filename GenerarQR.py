import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

# Función para generar el QR
def generar_qr():
    nombre_personal = entry_nombre.get()
    area_personal = entry_area.get()
    sueldo_diario = entry_sueldo.get()
    
    if not nombre_personal or not area_personal or not sueldo_diario:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    # Crear el contenido del código QR (Nombre, Área, Sueldo Diario)
    contenido_qr = f"{nombre_personal},{area_personal},{sueldo_diario}"
    
    # Generar el código QR
    qr_img = qrcode.make(contenido_qr)
    qr_img.save("codigo_qr.png")
    
    # Mostrar el código QR en la interfaz
    img = Image.open("codigo_qr.png")
    
    # Corregir el uso de ANTIALIAS
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
    
    qr_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=qr_tk)
    qr_label.image = qr_tk  # Mantener referencia para que no se borre la imagen
    
    messagebox.showinfo("Éxito", "Código QR generado correctamente")

# Función para centrar la ventana
def centrar_ventana(ventana):
    ventana.update_idletasks()  # Actualiza las tareas pendientes
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")

# Función para abrir la ventana de generación de QR
def abrir_ventana_qr(root):  # Añadir root como argumento
    global entry_nombre, entry_area, entry_sueldo, qr_label
    
    # Crear la ventana para generar el código QR
    ventana_qr = tk.Toplevel(root)
    ventana_qr.title("Generador de Código QR para Personal")
    
    # Crear los campos de entrada
    tk.Label(ventana_qr, text="Nombre del Personal:").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_qr)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_qr, text="Área del Personal:").grid(row=1, column=0, padx=10, pady=10)
    entry_area = tk.Entry(ventana_qr)
    entry_area.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_qr, text="Sueldo Diario:").grid(row=2, column=0, padx=10, pady=10)
    entry_sueldo = tk.Entry(ventana_qr)
    entry_sueldo.grid(row=2, column=1, padx=10, pady=10)

    # Botón para generar el QR
    btn_generar = tk.Button(ventana_qr, text="Generar Código QR", command=generar_qr)
    btn_generar.grid(row=3, columnspan=2, pady=20)

    # Label para mostrar el código QR
    qr_label = tk.Label(ventana_qr)
    qr_label.grid(row=4, columnspan=2, pady=10)

    # Centrar la ventana
    centrar_ventana(ventana_qr)

