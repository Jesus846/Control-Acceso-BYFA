import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import os


if not os.path.exists('QR_VISITAS'):
    os.makedirs('QR_VISITAS')

def centrar_ventana(ventana):
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{x}+{y}")


def generar_qr(entry_tarjeta, entry_usuario, lbl_qr_image):
    tarjeta = entry_tarjeta.get().strip()
    usuario = entry_usuario.get().strip()

    if not tarjeta or not usuario:
        messagebox.showwarning("Datos incompletos", "Por favor, complete todos los campos.")
        return

    qr_data = f"{tarjeta},{usuario}"

 
    nombre_archivo = obtener_nombre_archivo(usuario)


    qr = qrcode.make(qr_data)
    qr.save(nombre_archivo)

  
    img = Image.open(nombre_archivo)
    img = img.resize((150, 150))  
    qr_img = ImageTk.PhotoImage(img)
    lbl_qr_image.config(image=qr_img)
    lbl_qr_image.image = qr_img

    messagebox.showinfo("QR generado", f"Código QR de visita generado y guardado como '{nombre_archivo}'.")


def obtener_nombre_archivo(usuario):
    base_nombre = f"QR_VISITAS/qr_visita_{usuario}"
    contador = 1
    nombre_archivo = f"{base_nombre}.png"

    
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{base_nombre}_{contador}.png"
        contador += 1

    return nombre_archivo


def abrir_ventana_qr(ventana):
    ventana_qr = tk.Toplevel(ventana) 
    ventana_qr.title("Generador de QR para Visitas")
    ventana_qr.geometry("400x400")

   
    tk.Label(ventana_qr, text="Número de tarjeta:").pack(pady=5)
    entry_tarjeta = tk.Entry(ventana_qr, width=40)
    entry_tarjeta.pack(pady=5)


    tk.Label(ventana_qr, text="Usuario general:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_qr, width=40)
    entry_usuario.pack(pady=5)

  
    lbl_qr_image = tk.Label(ventana_qr)
    lbl_qr_image.pack(pady=10)


    btn_generar_qr = tk.Button(ventana_qr, text="Generar QR", command=lambda: generar_qr(entry_tarjeta, entry_usuario, lbl_qr_image))
    btn_generar_qr.pack(pady=20)

    centrar_ventana(ventana_qr) 


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Panel Principal")
    root.geometry("300x200")

    btn_abrir_qr = tk.Button(root, text="Abrir Generador de QR", command=lambda: abrir_ventana_qr(root))
    btn_abrir_qr.pack(pady=20)

    root.mainloop()
